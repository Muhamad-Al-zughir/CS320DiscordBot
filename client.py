# shbang
# Started 1/18/2023

import os

import discord
from discord import app_commands
from dotenv import load_dotenv
from discord.ui import Button, View
# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.
import scheduler.schedule as schedule

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

# spidergif command: After the running of the command the bot will respond by posting a funny spider gif
@tree.command(name = 'spidergif', description = 'Bot will post a funny spider gif')
async def spider_gif(interaction: discord.Interaction):
    await interaction.response.send_message('https://tenor.com/view/to-everyone-that-is-looking-for-this-spider-gif-gif-20691150')

# listProfiles command: After the running of the command the bot will respond by posting a funny spider gif
@tree.command(name = 'listprofiles', description = 'Bot will list out all the profiles created on this server')
async def list_profiles_cmd(interaction: discord.Interaction):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # grabbing the path of the json file for this server
    check_file_size = os.stat(path).st_size # grabbing the file size, if check_file_size is 0 that means the file is empty and thus can be ignored
    # checking file size
    if(check_file_size == 0):
        await interaction.response.send_message('No profiles have been created on this server!')
    else:
        # responding by printing out the profiles using discord embed features
        await schedule.list_profiles(interaction)

# client event to take place whenever the client joins a server.
# it will create a new json file in the scheduler directory to store the data associated with this newly joined guild
@client.event
async def on_guild_join(guild):
    path = "scheduler/" + str(guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory 
    try:
        open(path, "x")
        print("Making file" + path)
    # if the file exists
    except FileExistsError:
        print("File exists " + path)

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

# Code to respond to any messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
