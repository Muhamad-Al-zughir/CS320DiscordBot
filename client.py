# shbang
# Started 1/18/2023

import os

import discord
from discord import app_commands
from dotenv import load_dotenv
# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.

# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Implement all the slash commands here, write down whos is which.
@tree.command(name = "libgen", description = "Search for books")
@app_commands.describe(type="Please enter either \"author\" or \"title\"", search="Search, must be at least 3 characters")
async def basic_libgen(interaction, type: str, search: str): # Set the arguments here to get options on the slash commands.
    res = libby.handleValidation(type, search)
    if (res != True):
        await bm.send_msg(interaction, res)
    else:
        results = libby.basicSearch(type, search)
        strings = libby.formatResults(results)
        msg = '\n'.join(strings)
        await bm.send_msg(interaction, msg)
    reply = await client.wait_for('message')
    try:
        num = int(reply.content)
        if (num > len(strings) or num < 1): raise ValueError("outside bounds")
    except ValueError:
        await bm.follow_up(interaction, "Not a number between 1-" + str(len(strings))) # Need to use a follow up after initial sending
        return
    obj = results[num]
    links = libby.getLinksFor(obj)
    strings2 = libby.formatLinks(links)
    msg = '\n'.join(strings2)
    await bm.follow_up(interaction, msg)

# Add new slash commands beneath this
@tree.command(name = "libgen", description = "Search for books")

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
