import discord, json, asyncio, os
from discord.ext import commands
from trusted_users import get_trusted_users as trusted_users

if not os.path.isfile('./cogs/bannedwords.json'):
    with open('./cogs/bannedwords.json', 'w') as f:
        json.dump({'banned': []}, f, indent=4)

def read_config():
    with open('./cogs/bannedwords.json', 'r') as f:
        return json.load(f)

def edit_config(data):
	with open('./cogs/bannedwords.json', 'w') as f:
		json.dump(data, f, indent=4)


async def check_forbidden(message):
    if str(message.author.id) in trusted_users():
        return
    words = read_config()
    for word in words['banned']:
        if word in message.content:
            await message.author.send(f"Warning, you used the forbidden word: {word}")
            await asyncio.sleep(1)
            await message.delete()
            return


class Automod(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('The Automod cog was successfully loaded!')
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        else:
            await check_forbidden(message)


    # Commands
    @commands.command()
    async def banword(self, ctx, word):
        config = read_config()
        if str(ctx.message.author.id) in trusted_users():

            words = read_config()
            if str(word) not in words:
                words['banned'].append(str(word))
                edit_config(words)

                await ctx.send(f'Successfully added {word} to the banned words list!')
            else:
                await ctx.send(f'The word "{word}" is already banned')
        else:
            await ctx.send("You are not allowed to use this command.")

def setup(client):
    client.add_cog(Automod(client))
