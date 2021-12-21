import os
import sqlite3
import re

import requests
from twitchio.ext import commands

import config

BASIC_AUTH = os.getenv("SPOTIFY_BASIC_AUTH")


def get_credentials(streamer):
    credentials = None
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(
        "SELECT access_token, token_type, expires_in, refresh_token, scope, user_id from strolchibot_spotify where streamer = ?",
        (streamer,))
    if s := c.fetchone():
        credentials = {
            "access_token": s[0],
            "token_type": s[1],
            "expires_in": s[2],
            "refresh_token": s[3],
            "scope": s[4],
            "user_id": s[5],
        }

    conn.close()
    return credentials


def update_credentials(credentials, name):
    conn = sqlite3.connect("db.sqlite3")
    c = conn.cursor()
    c.execute(
        "UPDATE strolchibot_spotify set access_token = ? where streamer = ?",
        (credentials["access_token"], name,))
    conn.commit()
    conn.close()


def get_song(streamer):
    credentials = get_credentials(streamer)
    if credentials:
        response = requests.get("https://api.spotify.com/v1/me/player", headers={
            'Authorization': f'Bearer {credentials["access_token"]}'
        })

        if response.status_code == 204:
            return None

        player = response.json()

        if response.status_code == 401:
            refresh_token(streamer)
            return get_song(streamer)
        elif response.status_code == 200 and player.get("is_playing"):
            player = response.json()
            item = player['item']
            artists = ", ".join([artist['name'] for artist in item['artists']])
            name = item['name']
            album = item['album']['name']
            url = item['external_urls']['spotify']

            return {"name": name, "artists": artists, "album": album, "url": url}

    return None


def refresh_token(streamer):
    credentials = get_credentials(streamer)

    if credentials:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": f'{credentials["refresh_token"]}'
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {BASIC_AUTH}'
        }
        response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
        new_credentials = response.json()
        credentials["access_token"] = new_credentials["access_token"]
        update_credentials(credentials, streamer)


class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="streamer")
    async def cmd_streamer(self, ctx, streamer):
        if ctx.author.is_mod:
            streamer = streamer.lower()
            if re.match("^[a-z0-9äöüß]+$", streamer):
                config.set("streamer", streamer)
