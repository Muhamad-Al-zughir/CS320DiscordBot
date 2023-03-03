# shbang
# Started 1/18/2023

import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from discord.ui import Button, View
import youtube_dl
import ffmpeg
import json
import asyncio
# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.
import scheduler.schedule as schedule
import music.muzique as mzb

# setting up the needed intents
intents = discord.Intents.all()
intents.message_content = True          # setting message_content to True in order to read messages
client = discord.Client(intents=intents)

# tree which will hold all of the client commands
tree = app_commands.CommandTree(client)

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

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
    await interaction.response.send_message('https://media.discordapp.net/attachments/721098895152775288/1001770030352060456/image0.gif')

# listProfiles command: After the running of the command the bot will post all the profiles that have been created 10 profiles at a time. Users will be able to use buttons to view the other profiles if there are more than 10
@tree.command(name = 'listprofiles', description = 'Bot will list out all the profiles created on this server')
async def list_profiles_cmd(interaction: discord.Interaction):
    # responding by printing out the profiles using discord embed features
    await schedule.list_profiles(interaction)

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'addprofile', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(name="Name of the profile to be created (NAME MUST NOT ALREADY BE IN USE)", notes="Any important notes regarding the profile")
async def add_profile_cmd(interaction: discord.Interaction, name: str, notes: str):
    await schedule.add_profile(interaction, name, notes)

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'deleteprofile', description = 'Bot will delete a profile with the given name')
@app_commands.describe(name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)")
async def delete_profile_cmd(interaction: discord.Interaction, name: str):
    await schedule.delete_profile(interaction, name)

# addevent command: 
@tree.command(name = 'addevent', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(profile_name="Name of the profile for which the event should be added to", event_name="Name of the event to be added",
                        event_notes="Notes regarding the event", start_hour="The hour the event starts (must be integer between 0 and 23 inclusive)",
                        start_min="minute the event starts", end_hour="The hour the event ends at (must be integer between 0 and 23 inclusive)",
                        end_min="The minute which the event ends at", day="Enter a number 1-7 to represent the day of the week (1=Sunday, 7=saturday)")
async def add_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int, day: int):
    await schedule.add_event(interaction, profile_name, event_name, event_notes, start_hour, start_min, end_hour, end_min, day)

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'deleteevent', description = 'Bot will delete a event with the given name (if multiple events of same name exist bot will delete one of users choosing)')
@app_commands.describe(profile_name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)",
                       event_name="Name of event to be deleted (EVENT MUST ALREADY EXIST)")
async def delete_profile_cmd(interaction: discord.Interaction, profile_name: str, event_name: str):
    await schedule.delete_event(interaction, profile_name, event_name)

# Bot will join YouTube channel
@tree.command(name = 'move', description = 'Bot will join your voice channel')
async def move(interaction: discord.Interaction):     
    await mzb.move(interaction)

# Streams from a YouTube Link
@tree.command(name = 'play_yt', description = 'Bot will play from a valid YouTube Link')
async def play_youtube(interaction: discord.Interaction, url:str):
    await mzb.play_youtube(interaction,url,client)

# End Stream
@tree.command(name = 'clear', description = 'Bot will clear all playing music')
async def clear(interaction: discord.Interaction):
    await mzb.clear(interaction)

# Pause Stream and Unpause Stream
@tree.command(name = 'pause-unpause', description = 'Bot will pause the currently playing song or unpause if one was being played')
async def pause_yt(interaction: discord.Interaction):
    await mzb.pause_yt(interaction)

#   dropdown menu for character selection
@tree.command(name = "rp_menu", description = "menu options for rp game")
async def rp_dropdown_menu_cmd(interaction: discord.Interaction):
    await botgame.rp_dropdown_menu(interaction)
 #  ===========================================
 
 #   create rp for character game
@tree.command(name = "create_rp_character", description = "character creation for game")
async def rp_character_create_cmd(interaction: discord.Interaction):
    await botgame.rp_character_create(interaction)
 #  ==============================================

# client event to take place whenever the client joins a server.
# it will create a new json file in the scheduler directory to store the data associated with this newly joined guild
@client.event
async def on_guild_join(guild):
    path = "scheduler/" + str(guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory 
    try:
        file = open(path, "x")
        # initializing the json file with a list in order that we make easy appends to it
        listObj = []
        json.dump(listObj, file)
        print("Making file" + path)
        file.close()
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
