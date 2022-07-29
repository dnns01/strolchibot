import json

from twitchio.ext import commands


class Einkaufsliste(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items = []
        self.load()

    def load(self):
        try:
            file = open("einkaufsliste.json", mode="r")
            self.items = json.load(file)
        except:
            self.items = []
            self.save()

    def save(self):
        file = open("einkaufsliste.json", mode="w")
        json.dump(self.items, file)

    @commands.command(name="einkaufsliste")
    async def cmd_giveaway(self, ctx, add=None, *item):
        """ take part at the giveaway """

        if add == "add":
            item = " ".join(item)
            self.items.append(item)
        else:
            if len(self.items) > 0:
                msg = "Auf Marcus Einkaufsliste stehen folgende Dinge: "
                for item in self.items:
                    if len(msg) + len(item) >= 500:
                        await ctx.send(msg[:-2])
                        msg = ""

                    msg += item + ", "

                await ctx.send(msg[:-2])
            else:
                await ctx.send(f"Auf Marcus Einkaufsliste steht noch nix!")
