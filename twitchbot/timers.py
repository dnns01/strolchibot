import sqlite3

from twitchio.ext import commands, routines

from twitchbot import config


class Timers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.item = -1
        self.interval = config.get("timers_interval")

    @routines.routine(minutes=config.get("timers_interval"))
    async def timer_loop(self):
        new_interval = config.get("timers_interval")
        if new_interval != self.interval:
            self.interval = new_interval
            self.timer_loop.change_interval(minutes=self.interval)
        else:
            if streams := await self.bot.stream():
                conn = sqlite3.connect("db.sqlite3")

                c = conn.cursor()
                c.execute(f"SELECT text FROM strolchibot_timer where active = 1")
                timers = list(c.fetchall())
                conn.close()

                self.item = (self.item + 1) % len(timers)
                await self.bot.send_announce(self.bot.channel(), timers[self.item][0])
