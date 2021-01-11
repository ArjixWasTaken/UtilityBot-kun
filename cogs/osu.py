import discord, requests, json
from discord.ext import commands

class osu(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The osu! cog was successfully loaded!')

    # Commands
    @commands.command()
    async def osu(self, ctx, *, username):
        apikey = "OSU_API_KEY_GOES_HERE"
        headers = {"content-type": "application/json", "user-key": apikey}
        osu = requests.post(f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}", headers=headers).json()
        embed = discord.Embed()
        embed.title = osu[0]["username"]
        embed.url = "https://osu.ppy.sh/u/{}".format(osu[0]["user_id"])
        embed.set_footer(text="Powered by osu!")
        embed.add_field(name="Join date", value=osu[0]["join_date"][:10])
        embed.add_field(name="Accuracy", value=round(float(osu[0]["accuracy"][:6])))
        embed.add_field(name="Level", value=round(float(osu[0]["level"][:5])))
        embed.add_field(name="Ranked score", value=osu[0]["ranked_score"])
        embed.add_field(name="Rank", value=osu[0]["pp_rank"])
        embed.add_field(name="Country rank ({})".format(osu[0]["country"]), value=osu[0]["pp_country_rank"])
        embed.add_field(name="Playcount", value=osu[0]["playcount"])
        embed.add_field(name="Total score", value=osu[0]["total_score"])
        embed.add_field(name="Total hours played", value=round(int(osu[0]["total_seconds_played"])/3600))
        embed.set_thumbnail(url="https://a.ppy.sh/{}".format(osu[0]["user_id"]))
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(osu(client))
