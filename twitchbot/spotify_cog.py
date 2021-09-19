import json
import os

import requests
from twitchio.ext import commands


@commands.core.cog(name="SpotifyCog")
class SpotifyCog:
    def __init__(self, bot):
        self.bot = bot
        self.spotify_file = "spotify.json"
        self.basic_auth = os.getenv("BASIC_AUTH")
        self.spotify = {}
        self.load_spotify()
        self.streamer = None

    def load_spotify(self):
        spotify_file = open(self.spotify_file, mode='r')
        self.spotify = json.load(spotify_file)

    def save_spotify(self):
        spotify_file = open(self.spotify_file, mode='w')
        json.dump(self.spotify, spotify_file)

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
        response = requests.get("https://api.spotify.com/v1/me/player", headers={
            'Authorization': f'Bearer {self.spotify[self.streamer]["access_token"]}'
        })

        if response.status_code == 204:
            return None

        player = response.json()

        if response.status_code == 401 and player.get("error") and player.get("error").get(
                "message") == "The access token expired":
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
        else:
            return None

    def refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "refresh_token": f'{self.spotify[self.streamer]["refresh_token"]}'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.basic_auth}'
        }
        response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        credentials = response.json()
        self.spotify[self.streamer]["access_token"] = credentials["access_token"]
        self.save_spotify()

    @commands.command(name="streamer")
    async def cmd_streamer(self, ctx, streamer):
        if ctx.author.is_mod:
            self.streamer = streamer.lower()
