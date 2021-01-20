from datetime import datetime, timedelta

import requests
from twitchio.ext import commands


@commands.core.cog(name="ArminCog")
class Armin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="armin")
    async def cmd_armin(self, ctx):
        url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=Meldedatum+%3E%3D+TIMESTAMP+%272021-01-16%27+AND+NeuerFall+in+%281%2C+0%29&objectIds=&time=&resultType=standard&outFields=AnzahlFall%2CMeldeDatum%2C+NeuerFall&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=MeldeDatum&groupByFieldsForStatistics=AnzahlFall%2CMeldeDatum%2C+NeuerFall&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22AnzahlFall%22%2C%22outStatisticFieldName%22%3A%22cases%22%7D%5D&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=pjson&token="
        response = requests.get(url)

        data = response.json()
        cases_per_day = {}
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        count = 0

        for feature in data["features"]:
            melde_datum = datetime.fromtimestamp(feature["attributes"]['MeldeDatum'] / 1000)
            neuer_fall = feature["attributes"]["NeuerFall"]
            cases = feature["attributes"]["cases"]

            if yesterday == melde_datum.strftime("%Y-%m-%d") and neuer_fall == 0:
                continue

            if cases_per_day.get(melde_datum) is None:
                cases_per_day[melde_datum] = cases
            else:
                cases_per_day[melde_datum] = cases + cases_per_day.get(melde_datum)

        for date, case in cases_per_day.items():
            count += case

        await ctx.send(
            f"Es wurden schon {format(count, ',').replace(',', '.')} (+-100%) Neuinfektionen gemeldet, seit Kanzler-Elect Armin an der Macht ist. So klappt es nicht! strolchSauer")
