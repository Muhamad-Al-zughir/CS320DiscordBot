# shbang
# Started 1/18/2023

import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from discord.ui import Button, View
import youtube_dl
#import ffmpeg
import json
import asyncio
# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
#import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.
import scheduler.schedule as schedule
import music.muzique as mzb
import mathcalc.math as calc

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

# addevent command: 
@tree.command(name = 'addevent', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(profile_name="Name of the profile for which this event should be added to", event_name="Name of the event to be added",
                        event_notes="Notes regarding the event", start_hour="The hour the event starts (must be integer between 0 and 23 inclusive)",
                        start_min="minute the event starts", end_hour="The hour the event ends at (must be integer between 0 and 23 inclusive)",
                        end_min="The minute which the event ends at")
async def add_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int):
    await schedule.add_event(interaction, profile_name, event_name, event_notes, start_hour, start_min, end_hour, end_min)

##################### YOUTUBE FUNCTIONALITY #############################
# Member list of people in channel to be streamed to (used later)
streaming_members = {}

# YouTube options list set to best audio settings
# Setting options found from youtube-dl documentation
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
yt_params = {'format' :  'bestaudio/best'}
yt_streamObj = youtube_dl.YoutubeDL(yt_params)

# ffmpeg params set to disable video
# Settings found from https://ffmpeg.org/ffmpeg.html
ff_params = {'options': '-vn'}


# ** NOTE **
# Class YouTube_linkobj below is borrowed from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py 

class YouTube_linkobj(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source)
       
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_streamObj.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]       # 1st item in playlist index

        filename = data['url'] if stream else yt_streamObj.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ff_params), data=data)       # Return discord.ffmpegpcm audio class 

@tree.command(name = 'move', description = 'Bot will join your voice channel')
async def move(interaction: discord.Interaction):     
        try:
            await interaction.response.send_message(f'Joining...')                  # Sends attempt message to server
            local = interaction.guild                                               # Create local instances of guild and check for existence of voice client
            voicechan = local.voice_client      
            if voicechan is not None:                                               # Voice channel exists, move to caller's channel
                return await voicechan.move_to(interaction.user.voice.channel)

            await interaction.user.voice.channel.connect()                          # Establish connection after move



        except Exception as err:                                                    # Display general catch-all error for debug purposes
            print(err)

# Streams from a YouTube Link
@tree.command(name = 'play_yt', description = 'Bot will play from a valid YouTube Link')
async def play_youtube(interaction: discord.Interaction, url:str):

        print("Join being attempted ..")
        local = interaction.guild                                                  # Establish server context
        voicechan = local.voice_client                                             # Establish related voice channel
        
        if voicechan is not None:                                                  # Disconnect if the bot is already in a voicechannel
            print("Bot currently not in channel\nJoining...")
            await local.voice_client.disconnect()
        
        await interaction.user.voice.channel.connect()

        server = interaction.guild                                                 # Re-establish server context and voice client after connection
        voice_channel = server.voice_client                                       
        
        print("Before retrieving YouTube Object...")
        filename = await YouTube_linkobj.from_url(url, loop=client.loop, stream=True)

        print("Before Playing in channel...")
        voice_channel.play(filename)

        print("Before user-end interaction message...")
        await interaction.response.send_message(f'Now playing {filename.title}') 
               
        print("Reached here in command")                                           # Debug statements

# End Stream
@tree.command(name = 'clear', description = 'Bot will clear all playing music')
async def clear(interaction: discord.Interaction):
    server = interaction.guild
    voice_channel = server.voice_client

    await voice_channel.disconnect()
    await interaction.response.send_message(f'Music has been stopped')


# Pause Stream and Unpause Stream
@tree.command(name = 'pause-unpause', description = 'Bot will pause the currently playing song or unpause if one was being played')
async def pause_yt(interaction: discord.Interaction):
    
    vcstatus = interaction.guild.voice_client
    if vcstatus.is_playing():
        vcstatus.pause()
        await interaction.response.send_message('player is now paused')
    elif vcstatus.is_paused():
        vcstatus.resume()
        await interaction.response.send_message('player is now un-paused')
    else:
        await interaction.response.send_message('Nothing is currently playing')

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

# # Code to respond to messages sent by users
# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return
        
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

#     if message.content.startswith('/chiefkeef'):
#         await message.channel.send("Fuckers in school telling me, always in the barber shop Chief Keef ain’t bout this, Chief Keef ain’t bout that My boy a BD on fucking Lamron and them He, he they say that nathan don’t be putting in no work SHUT THE FUCK UP! Y'all nathans ain’t know shit All ya motherfuckers talk about Chief Keef ain’t no hitta Chief Keef ain’t this Chief Keef a fake SHUT THE FUCK UP Y'all don’t live with that nathan Y'all know that nathan got caught with a ratchet Shootin' at the police and shit Nathan been on probation since fuckin, I don’t know when! Motherfuckers stop fuckin' playin' him like that Them nathans savages out there If I catch another motherfucker talking sweet about Chief Keef I’m fucking beating they ass! I’m not fucking playing no more You know those nathans role with Lil' Reese and them.")

#     if message.content.startswith('$bye'):
#         await message.channel.send('Bye!')
    
#     # await client.process_commands(message)

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

@tree.command(name = "equation", description = "Simple equation")
@app_commands.describe(simple = "Please enter a simple equation with each spaces in between")
async def equation(interaction: discord.Interaction, simple: str):
    equation = list(simple.split(" "))
    #print(equation)
    if not calc.simpleCheck(equation):
        interaction.send("The equation sent in not a valid simple equation. Try again.")
    #result = checker(equation)
    await interaction.response.send_message(calc.checker(equation))
 
# Code to respond to any messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
