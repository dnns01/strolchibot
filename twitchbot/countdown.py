from asyncio import sleep
from datetime import datetime

from twitchio.ext import commands, routines


class Countdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.timer.start()
        self.until = datetime(year=2022, month=4, day=5, hour=20)

    @routines.routine(minutes=1)
    async def timer(self):
        now = datetime.now()
        diff = (self.until - now).seconds // 60 + 1

        if diff > 0:
            await self.bot.channel().send(str(diff))

    @timer.before_routine
    async def timer_before(self):
        await sleep(60 - datetime.now().second)
