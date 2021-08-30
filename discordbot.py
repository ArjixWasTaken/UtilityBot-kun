from trusted_users import get_trusted_users as trusted_users
from discord.ext import tasks, commands
import requests
import asyncio
import discord
import random
import json
import os


BOT_TOKEN = 'BOT_TOKEN_GOES_HERE'


def run(client):
    client.run(BOT_TOKEN)


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if str(message.guild.id) in prefixes:
        return prefixes[str(message.guild.id)]
    else:
        return 'ap!'


client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')

extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and 'getanime' not in filename:
        client.load_extension(f'cogs.{filename[:-3]}')
        extensions.append(filename[:-3])
commandss = []
for extension in extensions:
    try:
        with open(os.path.join('./cogs', extension + '.json'), 'r') as f:
            helpm = json.loads(f.read())['help']
            for key, value in helpm.items():
                entry = [key, value]
                commandss.append(entry)
    except Exception as e:
        print("Error: " + str(e))


@client.command()
async def help(ctx):
    embed = discord.Embed(color=0x00ff00)
    embed.set_author(name='Help')
    for a in commandss:
        embed.add_field(inline=False, name=a[0], value=a[1])
    embed.add_field(inline=False, name='ping',
                    value='Returns the ping of the bot.')
    embed.add_field(inline=False, name='help',
                    value='Lists all the available commands the bot offers.')
    await ctx.send(embed=embed)


# events

# on_connect()


@client.event
async def on_connect():
    print('Bot is connecting...')

# on_ready()


@client.event
async def on_ready():
    print('Discord bot is ready.')

# on_message()


@client.event
async def on_message(message):
    # Checks if message sent by himself
    if message.author == client.user:
        return
    # Checks if mentioned
    if client.user in message.mentions:
        await message.channel.send("Utility bot reports to duty, Sir!. My prefix is " + command_prefix)

    await client.process_commands(message)

# on_member_join()

""" This here sends a welcome message to any user that joins the server...so i left it as an example
@client.event
async def on_member_join(member):
    guild = client.get_guild(737374502689964172)
    if member.guild == guild:
        embed = discord.Embed(color=0x00ff00)
        emoji = client.get_emoji(741774114754396311)
        embed.title = 'Welcome to x!'
        message = "Welcome to my server!"
        embed.description = message
        await member.send(embed=embed)
"""
# commands


@client.command(aliases=['prefix'])
async def setprefix(ctx, *, prefix):
    trusted = trusted_users()
    if ctx.message.author.guild_permissions.manage_channels or ctx.author.id in trusted:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        await ctx.send('**Successfully changed the prefix to *{}***'.format(prefix))
    else:
        await ctx.send('**You do not have enough permissions to use that command.**')


@client.command()
async def warn(ctx, user: discord.User, *, message):
    '''
    this command doesnt actually warn people, it just sends the message
    '''
    embed = discord.Embed(color=0x00ff00)
    message = '***{} has been warned.*** **|| {}**'.format(
        user.mention, message)
    embed.description = message
    await ctx.send(embed=embed)


# Ping utility
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

# Creates an embed and returns it.


def mk_embed(title, link, description):
    embed = discord.Embed(color=0x00ff00)
    embed.title = title
    embed.url = link
    embed.description = description
    return embed


run(client)
