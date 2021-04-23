import random

from twitchio.ext import commands


@commands.core.cog(name="Giveaway")
class Giveaway:
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_enabled = False
        self.giveaway_entries = {}

    @commands.command(name="gierig")
    async def cmd_giveaway(self, ctx):
        """ take part at the giveaway """

        texts = [f"{ctx.author.name} ist ein gieriger Gierlappen!", f"Geil!!! {ctx.author.name} giert hart rein!",
                 f"So klappt es doch {ctx.author.name}! Einmal hart reingieren."]

        if self.giveaway_enabled:
            if self.giveaway_entries.get(ctx.author.name) != 1:
                await self.bot.send_me(ctx, random.choice(texts), "YellowGreen")
                self.giveaway_entries[ctx.author.name] = 1

    @commands.command(name="giveaway")
    async def cmd_giveaway_open(self, ctx, param):
        """ Reset and Open the giveaway """

        if ctx.author.is_mod:
            if param == "open":
                self.giveaway_enabled = True
                self.giveaway_entries = {}
                await self.bot.send_me(ctx,
                                       "Das Giveaway wurde gestartet. Schreibe !gierig in den Chat um daran teilzunehmen.",
                                       "YellowGreen")
            elif param == "close":
                self.giveaway_enabled = False
                await self.bot.send_me(ctx, "Das Giveaway wurde geschlossen. Es kann niemand mehr teilnehmen.",
                                       "YellowGreen")
            elif param == "draw":
                if len(self.giveaway_entries) > 0:
                    winner = random.choice(list(self.giveaway_entries))
                    entry_count = len(self.giveaway_entries)
                    del self.giveaway_entries[winner]
                    await self.bot.send_me(ctx,
                                           f"Es wurde aus {entry_count} Einträgen ausgelost. Und der Gewinner ist... @{winner}",
                                           "YellowGreen")
                else:
                    await self.bot.send_me(ctx, "Es muss Einträge geben, damit ein Gewinner gezogen werden kann.",
                                           "YellowGreen")
