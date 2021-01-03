import os
import random
import sqlite3
from abc import ABC
from time import sleep, time
from dotenv import load_dotenv
import requests
from twitchio.dataclasses import Context, Message, Channel
from twitchio.ext import commands
from giveaway_cog import GiveawayGog
from klassenbuch_cog import KlassenbuchCog
from spotify_cog import SpotifyCog
from vote_cog import VoteCog

load_dotenv()


class StrolchiBot(commands.Bot, ABC):
    def __init__(self):
        self.IRC_TOKEN = os.getenv("IRC_TOKEN")
        self.CLIENT_ID = os.getenv("CLIENT_ID")
        self.CLIENT_SECRET = os.getenv("CLIENT_SECRET")
        self.NICK = os.getenv("NICK")
        self.CHANNEL = os.getenv("CHANNEL")
        self.PREFIX = os.getenv("PREFIX")
        self.BATI_PROBABILITY = float(os.getenv("BATI_PROBABILITY"))
        self.BATI_KAPPA_PROBABILITY = float(os.getenv("BATI_KAPPA_PROBABILITY"))
        self.BATI_DELAY = int(os.getenv("BATI_DELAY"))
        self.last_bati = 0
        super().__init__(irc_token=self.IRC_TOKEN, prefix=self.PREFIX, nick=self.NICK, initial_channels=[self.CHANNEL],
                         client_id=self.CLIENT_ID, client_secret=self.CLIENT_SECRET)
        self.add_cog(GiveawayGog(self))
        self.add_cog(VoteCog(self))
        self.add_cog(KlassenbuchCog(self))
        self.add_cog(SpotifyCog(self))

    @staticmethod
    async def send_me(ctx, content, color):
        """ Change Text color to color and send content as message """

        if type(ctx) is Context or type(ctx) is Channel:
            await ctx.color(color)
            await ctx.send_me(content)
        elif type(ctx) is Message:
            await ctx.channel.color(color)
            await ctx.channel.send_me(content)

    async def event_ready(self):
        print('Logged in')

    @staticmethod
    def get_percentage(part, total):
        """ Calculate percentage """
        if total != 0:
            return round(part / total * 100, 1)

        return 0

    def channel(self):
        return self.get_channel(self.CHANNEL)

    async def chatters(self):
        return await self.get_chatters(self.CHANNEL)

    async def stream(self):
        return await self.get_stream(self.CHANNEL)


bot = StrolchiBot()


@bot.command(name="sounds")
async def cmd_sounds(ctx):
    response = requests.get("https://api.robotredford.com/v1/command/indiestrolche/sound")
    sounds = list(dict.fromkeys([command["command"] for command in response.json()]))
    sounds.sort()
    print(sounds)
    answer = f"Kenner*innen fahren folgende Manöver im Chat: 🔊 "

    for sound in sounds:
        cmd = "!" + sound + ", "
        if len(answer) + len(cmd) > 500:
            await ctx.send(answer[:-2] + " 🔊")
            answer = f"🔊 "

        answer += cmd

    await ctx.send(answer[:-2] + " 🔊")


@bot.listen("event_message")
async def bati(message):
    if message.author == "bati_mati":
        if ("kappa" in message.content.lower() and random.random() < bot.BATI_KAPPA_PROBABILITY) \
                or (random.random() < bot.BATI_PROBABILITY and time() >= bot.last_bati + (bot.BATI_DELAY * 3600)):
            sleep(random.random())
            await bot.channel().send("bati")
            bot.last_bati = time()


@bot.listen("event_message")
async def process_text_commands(message):
    if message.author.name.lower() == bot.NICK.lower():
        return

    if message.content[0] == "!":
        command = message.content.split(" ")[0][1:]
        conn = sqlite3.connect("db.sqlite3")

        c = conn.cursor()
        c.execute('SELECT text from strolchibot_textcommand where command = ?', (command,))
        texts = c.fetchall()
        if len(texts) > 0:
            text = random.choice(texts)[0]
            await message.channel.send(text)
        conn.close()


bot.run()
