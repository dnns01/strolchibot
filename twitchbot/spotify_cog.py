import os
import sqlite3

import requests
from twitchio.ext import commands


class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.basic_auth = os.getenv("SPOTIFY_BASIC_AUTH")
        self.streamer = None

    def get_streamer(self, name):
        streamer = None
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(
            "SELECT access_token, token_type, expires_in, refresh_token, scope, user_id from strolchibot_spotify where streamer = ?",
            (name,))
        if s := c.fetchone():
            streamer = {
                "access_token": s[0],
                "token_type": s[1],
                "expires_in": s[2],
                "refresh_token": s[3],
                "scope": s[4],
                "user_id": s[5],
            }

        conn.close()
        return streamer

    def update_streamer(self, streamer, name):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute(
            "UPDATE strolchibot_spotify set access_token = ? where streamer = ?",
            (streamer["access_token"], name,))
        conn.commit()
        conn.close()

    @commands.command(name="song")
    async def cmd_song(self, ctx):
        if self.streamer:
            song = self.get_song()

            if song:
                await ctx.send(
                    f"catJAM 🎶Bei {self.streamer.capitalize()} läuft gerade der kultige Song \"{song['name']}\" von \"{song['artists']}\" aus dem Album \"{song['album']}\"🎶. Einfach selbst mal einknipsen: {song['url']}")
            else:
                await ctx.send(
                    f"Woher soll ich denn wissen, was gerade läuft? Frag doch selbst nach!")

        else:
            await ctx.send(
                "Ich würde ja gerne sagen, welcher kultige Song gerade läuft. Leider hat mir noch keiner gesagt, wer eigentlich gerade streamt strolchWut")

    def get_song(self):
        streamer = self.get_streamer(self.streamer)
        if streamer:
            response = requests.get("https://api.spotify.com/v1/me/player", headers={
                'Authorization': f'Bearer {streamer["access_token"]}'
            })

            if response.status_code == 204:
                return None

            player = response.json()

            if response.status_code == 401:
                self.refresh_token()
                return self.get_song()
            elif response.status_code == 200 and player.get("is_playing"):
                player = response.json()
                item = player['item']
                artists = ", ".join([artist['name'] for artist in item['artists']])
                name = item['name']
                album = item['album']['name']
                url = item['external_urls']['spotify']

                return {"name": name, "artists": artists, "album": album, "url": url}

        return None

    def refresh_token(self):
        streamer = self.get_streamer(self.streamer)

        if streamer:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": f'{streamer["refresh_token"]}'
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {self.basic_auth}'
            }
            response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
            credentials = response.json()
            streamer["access_token"] = credentials["access_token"]
            self.update_streamer(streamer, self.streamer)

    @commands.command(name="streamer")
    async def cmd_streamer(self, ctx, streamer):
        if ctx.author.is_mod:
            self.streamer = streamer.lower()
