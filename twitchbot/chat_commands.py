import random
import re
import sqlite3

from twitchio.ext import commands

import spotify_cog
import config

DB_PATH = "db.sqlite3"


def check_permissions(message, permissions):
    if permissions == "EO":
        return True
    elif permissions == "SUB":
        return message.author.is_subscriber or message.author.is_mod
    elif permissions == "MOD":
        return message.author.is_mod

    return False


class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.event()
    async def event_message(self, message):
        if not message.author or message.author.name.lower() == self.bot.NICK.lower():
            return

        if message.content[0] == "!":
            msg = message.content.split(" ")
            command = msg[0][1:]
            args = msg[1:]

            conn = sqlite3.connect(DB_PATH)

            c = conn.cursor()
            c.execute('SELECT text, permissions from strolchibot_command where command = ? and active is true',
                      (command,))
            eligible_commands = c.fetchall()
            conn.close()
            if len(eligible_commands) > 0:
                cmd = random.choice(eligible_commands)
                if check_permissions(message, cmd[1]):
                    text = self.process_variables(cmd[0], args)
                    await message.channel.send(text)

    def process_variables(self, text, args):
        variables = re.findall("\{[\w\d\s+-]+}", text)
        spotify = None

        for variable in variables:
            tokens = variable[1:-1].split()
            if tokens[0] == "count" or tokens[0] == "getcount":
                count = self.process_counter(tokens[0], tokens[1:])
                text = text.replace(variable, str(count))
            elif tokens[0] == "spotify":
                if value := self.process_spotify(tokens[1], spotify):
                    text = text.replace(variable, value)
                else:
                    return "Woher soll ich denn wissen, was gerade läuft? Frag doch selbst nach!"
            elif tokens[0] == "streamer":
                streamer = self.process_streamer()
                if streamer:
                    text = text.replace(variable, streamer.capitalize())
            elif tokens[0] == "args" and len(tokens) == 2:
                arg = self.process_args(args, tokens[1])
                if arg:
                    text = text.replace(variable, arg)
        return text

    def process_counter(self, var_name, params):
        counter_name = params[0]
        counter = self.get_count(counter_name)

        if var_name == "count":
            if len(params) == 2:
                if params[1][0] == "+":
                    counter += int(params[1][1:])
                elif params[1][0] == "-":
                    counter -= int(params[1][1:])
                else:
                    counter = int(params[1])
            else:
                counter += 1

            self.set_count(counter_name, counter)

        return counter

    def get_count(self, name):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('SELECT count from strolchibot_counter where name = ?', (name,))
        count = c.fetchone()
        conn.close()
        if count:
            return count[0]
        else:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute('INSERT INTO strolchibot_counter(name, count) VALUES (?, ?)', (name, 0))
            conn.commit()
            conn.close()
            return 0

    def set_count(self, name, count):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('UPDATE strolchibot_counter set count = ? where name = ?', (count, name))
        conn.commit()
        conn.close()

    def process_spotify(self, param, song):
        if not song:
            song = spotify_cog.get_song(self.process_streamer())

        if song:
            if value := song.get(param):
                return value
            else:
                return None
        else:
            return None

    def process_streamer(self):
        return config.get("streamer")

    def process_args(self, args, index):
        try:
            index = int(index)
        except ValueError:
            index = 0

        if len(args) > index:
            return args[0]

        return None
