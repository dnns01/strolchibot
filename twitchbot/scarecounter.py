from twitchio.ext import commands


class ScareCounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scarecount = 0

    @commands.command(name="scarecount")
    async def cmd_scarecount(self, ctx, add=None):
        if add == "++":
            self.scarecount += 1
        elif add == "--":
            self.scarecount -= 1

        await ctx.send(f"Shawna und Marcus haben sich schon {self.scarecount} mal geBRRRRRRRRt 👻👻👻")
