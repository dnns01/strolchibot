from twitchio.ext import commands


@commands.core.cog(name="ScareCounter")
class ScareCounter:
    def __init__(self, bot):
        self.bot = bot
        self.scarecount = 11

    @commands.command(name="scarecount")
    async def cmd_scarecount(self, ctx, add=None):
        if add == "++":
            self.scarecount += 1
        elif add == "--":
            self.scarecount -= 1

        await ctx.send(f"Shawna und Marcus haben sich schon {self.scarecount} mal gegruselt 👻👻👻")
