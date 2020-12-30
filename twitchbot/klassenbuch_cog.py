import sqlite3
from twitchio.ext import commands


@commands.core.cog(name="KlassenbuchCog")
class KlassenbuchCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sticker")
    async def cmd_sticker(self, ctx, name=None):
        if name:
            if name[0] == "@":
                name = name[1:]
        else:
            name = ctx.author.name

        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT sticker from strolchibot_klassenbuch where name = ?', (name,))
        sticker = c.fetchone()

        if not sticker:
            sticker = (0,)

        await ctx.send(f"{name} hat {sticker[0]} Sticker")
        conn.close()

    @commands.command(name="klassenbuch")
    async def cmd_klassenbuch(self, ctx):
        conn = sqlite3.connect("db.sqlite3")
        c = conn.cursor()
        c.execute('SELECT name, sticker from strolchibot_klassenbuch order by sticker desc')
        klassenbuch = c.fetchall()

        answer = f"Im Klassenbuch stehen aktuell folgende Einträge: "
        for entry in klassenbuch:
            entry_str = f"{entry[0]} hat {entry[1]} Sticker,"
            if len(answer) + len(entry_str) > 500:
                await ctx.send(answer[:-1])
                answer = entry_str
            else:
                answer += entry_str

        await ctx.send(answer[:-1])
        conn.close()
