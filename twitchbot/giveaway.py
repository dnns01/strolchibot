import random

from twitchio.ext import commands, routines


class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_enabled = False
        self.giveaway_entries = {}
        self.just_started = False

    @commands.command(name="gierig")
    async def cmd_giveaway(self, ctx):
        """ take part at the giveaway """

        texts = [f"{ctx.author.name} ist ein strolchG ieriger strolchG ierlappen!", 
                 f"Geil!!! {ctx.author.name} strolchG iert hart rein!",
                 f"So klappt es doch {ctx.author.name}! Einmal hart rein strolchG ieren.", 
                 f"Spieglein, Spieglein an der Wand, wer ist am strolchG ierigsten im ganzen Land? Oh Königin {ctx.author.name} strolchG iert am härtesten hier.",
                 f"strolchG IERMASTER3000 {ctx.author.name} ist am Start!"]

        if self.giveaway_enabled:
            if self.giveaway_entries.get(ctx.author.name) != 1:
                await self.bot.send_me(ctx, random.choice(texts))
                self.giveaway_entries[ctx.author.name] = 1

    @commands.command(name="giveaway")
    async def cmd_giveaway_open(self, ctx, param=None):
        """ Reset and Open the giveaway """

        if param is None:
            if self.giveaway_enabled:
                entry_count = len(self.giveaway_entries)
                await self.bot.send_me(ctx,
                                       f"j@@@@ gerade läuft ein strolchG iveaway. Sei auch du ein strolchG ieriger strolchG ierlappen, indem "
                                       f"du !gierig in den Chat schreibst. Es haben bereits {entry_count} andere hart "
                                       f"reingegiert!")

            else:
                await self.bot.send_me(ctx,
                                       "Gerade läuft leider kein Giveaway. Später vielleicht")
            return
        if ctx.author.is_mod:
            if param == "open":
                self.giveaway_enabled = True
                self.giveaway_entries = {}
                self.just_started = True
                self.giveaway_loop.start()
                await self.bot.send_announce(ctx,
                                             "Das Giveaway wurde gestartet. Schreibe !gierig in den Chat um daran "
                                             "teilzunehmen.")
            elif param == "close":
                self.giveaway_enabled = False
                self.giveaway_loop.stop()
                await self.bot.send_announce(ctx, "Das Giveaway wurde geschlossen. Es kann niemand mehr teilnehmen.")
            elif param == "draw":
                entry_count = len(self.giveaway_entries)
                if entry_count > 0:
                    winner = random.choice(list(self.giveaway_entries))
                    del self.giveaway_entries[winner]
                    msg = f"Es wurde aus {entry_count} Einträgen ausgelost. Und der Gewinner ist... @{winner}" \
                        if entry_count > 1 \
                        else f"Es gab nur eine Person im Lostopf. Natürlich ist der Gewinner @{winner}... " \
                             f"Woooow... was eine Überraschung"
                    await self.bot.send_announce(ctx, msg)
                else:
                    await self.bot.send_announce(ctx, "Niemand in der Lostrommel, um gezogen zu werden..")

    @routines.routine(minutes=5)
    async def giveaway_loop(self):
        if self.giveaway_enabled:
            if self.just_started:
                self.just_started = False
            else:
                entry_count = len(self.giveaway_entries)
                await self.bot.send_announce(self.bot.channel(),
                                             f"Einfach nur Krank!!! Hier wird schon wieder übelster Schrott rausgehauen. "
                                             f"Es haben bereits {entry_count} Zuschis ihren Namen in den Lostopf geworfen. "
                                             f"Schreibe JETZT !gierig in den Chat, um auch am Giveaway teilzunehmen!")
