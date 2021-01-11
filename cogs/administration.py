import discord, requests, random
from discord.ext import commands
import json
from trusted_users import get_trusted_users as trusted_users

if not os.path.isfile('./roasts.json'):
    with open('./roasts.json', 'w') as f:
        json.dump({'roast_list': []}, f, indent=4)

def getRoast():
    with open('./roasts.json', 'r') as f:
        data = json.loads(f.read())
    return data

def WriteRoast(data):
    with open('./roasts.json', 'w') as f:
        json.dump(data, f, indent=4)

class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Administration cog was successfully loaded!')

    @commands.command()
    async def roast(self, ctx, user: discord.User):
        roasts = getRoast()['roast_list']
        message = random.choice(roasts).format(user.mention)
        await ctx.send(message)

    @commands.command()
    async def roasts(self, ctx):
        roasts = getRoast()['roast_list']
        message = json.dumps(roasts, indent=3)
        await ctx.send(message)

    @commands.command(aliases=['roast-add'])
    async def add_roast(self, ctx, *, roast):
        if str(ctx.author.id) in trusted_users():
            roasts = getRoast()
            roasts['roast_list'].append(roast)
            WriteRoast(roasts)
            await ctx.send(f"**{roast}** was successfuly added.")
        else:
            await ctx.send("Couldn't register the roast, you are not in the **Trusted** list.")


def setup(client):
    client.add_cog(Admin(client))
