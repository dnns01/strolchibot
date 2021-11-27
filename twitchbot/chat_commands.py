import random
import re
import sqlite3

from twitchio.ext import commands


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

            conn = sqlite3.connect("db.sqlite3")

            c = conn.cursor()
            c.execute('SELECT text from strolchibot_command where command = ? and active is true', (command,))
            texts = c.fetchall()
            conn.close()
            if len(texts) > 0:
                text = random.choice(texts)[0]
                text = self.process_variables(text, args)
                await message.channel.send(text)

    def process_variables(self, text, args):
        variables = re.findall("\{[\w\d\s+-]+}", text)

        for variable in variables:
            tokens = variable[1:-1].split()
            print(tokens[4:])
            if tokens[0] == "count" or tokens[0] == "getcount":
                count = self.process_counter(tokens[0], tokens[1:])
                text = text.replace(variable, str(count))

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
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT count from strolchibot_counter where name = ?', (name,))
        count = c.fetchone()
        conn.close()
        if count:
            return count[0]
        else:
            conn = sqlite3.connect("db.sqlite3")
            c = conn.cursor()
            c.execute('INSERT INTO strolchibot_counter(name, count) VALUES (?, ?)', (name, 0))
            conn.commit()
            conn.close()
            return 0

    def set_count(self, name, count):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('UPDATE strolchibot_counter set count = ? where name = ?', (count, name))
        conn.commit()
        conn.close()
