# shbang
# Started 1/18/2023

import os
import sys
import discord
from discord import app_commands
from dotenv import load_dotenv
import json

# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib_handler as lb
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

# HELP COMMAND STRINGS
# MUSIC

musicString1 = "```**Music**\nmove: Moves a bot to a voice channel if you are already located in one"
musicString2 = "\nplay: Plays from a YouTube, Soundcloud, Or Spotify Link, or a general search query"
musicString3 = "\nclear: clears all songs from queue and leaves voice channel"
musicString4 = "\npause-unpause: pauses song if currently playing, unpauses if paused already"
musicString5 = "\nskip: skips currently playing song"
musicString6 = "\nqueue: Displays currently queued songs in order"
musicString7 = "\nshuffle: Shuffles current queue of music into random order"
musicString8 = "\nshiftsong: Shifts song to set time in track"
musicString9 = "\nencore: Repeats currently playing song"
musicString10 ="\nswap: swaps two indexes of a queue"
musicString11 ="\ndisplayInfo: displays YouTube Info of currently playing song"
musicString12 ="\ndisplayLyrics: displays Lyrics of currently playing song if available"
musicString13 ="\nshiftsong_percent: Shifts song to a set percentage in track"
musicString14 ="\naddplaylist: adds YouTube playlist to queue ONLY if there is a currently playing song"
musicString15 ="\naboutthealbum: displays information about the album if the track belongs to one"
musicString16 ="\nabouttheartist: displays information about the artist if it can be found (Wikipedia)"
musicString17 ="\naboutthesong: displays information about the song if there is information on it (Wikipedia)```"
musicString = musicString1 + musicString2 + musicString3 + musicString4 + musicString5 + musicString6 + musicString7 + musicString8 + musicString9 + musicString10 + musicString11 + musicString12 + musicString13 + musicString14 + musicString15 + musicString16 + musicString17


# Implement all the slash commands here, write down whos is which.
@tree.command(name = "libgen", description = "Search for books")
@app_commands.describe(type="Please enter either \"author\" or \"title\"", search="Search, must be at least 3 characters")
async def basic_libgen(interaction, type: str, search: str): # Set the arguments here to get options on the slash commands.
    await lb.handleLibSearch(interaction, type, search)


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

# viewprofile command: After the running of the command the bot will list out all of the events of a given profile with the list of events for each given day of the week. 
@tree.command(name = 'viewprofile', description = 'Bot will list out all the profiles created on this server')
@app_commands.describe(name="Name of the profile to be viewed (PROFILE MUST EXIST)")
async def view_profile_cmd(interaction: discord.Interaction, name: str): 
    # responding by printing out the profiles using discord embed features
    await schedule.view_profile(interaction, name)

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'addprofile', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(name="Name of the profile to be created (NAME MUST NOT ALREADY BE IN USE)", notes="Any important notes regarding the profile")
async def add_profile_cmd(interaction: discord.Interaction, name: str, notes: str):
    await schedule.add_profile(interaction, name, notes)

# deleteprofile command: Takes in profile name. After running the command the bot will delete the profile with the given name
# Name of the profile must be of an existing profile
@tree.command(name = 'deleteprofile', description = 'Bot will delete a profile with the given name')
@app_commands.describe(name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)")
async def delete_profile_cmd(interaction: discord.Interaction, name: str):
    await schedule.delete_profile(interaction, name)

# addevent command: 
@tree.command(name = 'addevent', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(profile_name="Name of the profile for which the event should be added to", event_name="Name of the event to be added",
                        event_notes="Notes regarding the event", start_hour="The hour the event starts (must be integer between 0 and 23 inclusive)",
                        start_min="minute the event starts", end_hour="The hour the event ends at (must be integer between 0 and 23 inclusive)",
                        end_min="The minute which the event ends at", day="Enter a number 1-7 to represent the day of the week (1=Sun, 2=Mon, 3=Tue, 4=Wed, 5=Thu, 6=Fri, 7=saturday)")
async def add_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int, day: int):
    await schedule.add_event(interaction, client, profile_name, event_name, event_notes, start_hour, start_min, end_hour, end_min, day)

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'deleteevent', description = 'Bot will delete a event with the given name')
@app_commands.describe(profile_name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)",
                       event_name="Name of event to be deleted (EVENT MUST ALREADY EXIST)")
async def delete_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str):
    await schedule.delete_event(interaction, client, profile_name, event_name)

# googlecalendar
@tree.command(name = 'googlecalendar', description = 'Takes the given profile name and creates a visual weekly schedule using google calendar')
@app_commands.describe(profile_name="Name of the profile to be used")
async def google_calendar_cmd(interaction: discord.Interaction, profile_name: str):
    await interaction.response.defer()
    await schedule.google_calendar(interaction, profile_name)
    os.remove("myscreenshot.png")
    os.remove("mycroppedscreenshot.png")

# Bot will join Discord Voice channel
@tree.command(name = 'move', description = 'Bot will join your voice channel')
async def move(interaction: discord.Interaction):     
    await mzb.move(interaction)

# Streams from a YouTube, SoundCloud, or Spotify Link
@tree.command(name = 'play', description = 'Enter a valid YouTube, SoundCloud, or Spotify Link')
async def play(interaction: discord.Interaction, url:str):
    await mzb.play(interaction,url,client)
    
# End Stream
@tree.command(name = 'clear', description = 'Bot will clear all playing music')
async def clear(interaction: discord.Interaction):
    await mzb.clear(interaction)

# Pause Stream and Unpause Stream
@tree.command(name = 'pause-unpause', description = 'Bot will pause the currently playing song or unpause if one was being played')
async def pause_yt(interaction: discord.Interaction):
    await mzb.pause_yt(interaction)

# Skip currently playing song
@tree.command(name = 'skip', description = 'Bot will skip the currently playing song')
async def skipSong(interaction: discord.Interaction):
    await mzb.skipSong(interaction, client)

# Display current queue 
@tree.command(name = 'queue', description = 'Display the current active music queue')
async def displayQueue(interaction: discord.Interaction):
    await mzb.displayQueue(interaction, client)

# Shuffle Current Queue
@tree.command(name = 'shuffle', description = 'Shuffle and display current active music queue')
async def shuffleQueue(interaction: discord.Interaction):
    await mzb.shuffleQueue(interaction, client)

# Shift song for a certan value in seconds 
@tree.command(name = 'shiftsong', description = 'Shift a song forward or backward for a valid number of seconds')
async def fastForwardSong(interaction: discord.Interaction, seconds: int):
    await mzb.fastForwardSong(interaction, client, seconds)

# Repeat a song
@tree.command(name = 'encore', description = 'Repeat the currently playing song')
async def encore(interaction: discord.Interaction):
    await mzb.encore(interaction,client)

# Swap Two Indexes for a Song queue
@tree.command(name = 'swap', description = 'Swap two indexes of a queue')
async def swap(interaction: discord.Interaction, indexone: int, indextwo: int):
    await mzb.swap(interaction,client,indexone,indextwo)

# Display Song Informatiom
@tree.command(name = 'displayinfo', description = 'Display information about the current song / video')
async def swap(interaction: discord.Interaction):
    await mzb.displayInfo(interaction,client)

# Display Song Lyrics
@tree.command(name = 'displaylyrics', description = 'Display Lyrics for the current playing song')
async def displayLyrics(interaction: discord.Interaction):
    await mzb.displayLyrics(interaction,client)

# Shift song for a certain percentage value of total runtime
@tree.command(name = 'shiftsong_percent', description = 'Shift to a certain percentage of the total runtime of the current track')
async def percentageShift(interaction: discord.Interaction, percent: int):
    await mzb.percentageShift(interaction, client, percent)

@tree.command(name = 'addplaylist', description = 'add a youtube playlist to queue')
async def addPlaylist(interaction: discord.Interaction, url: str):
    await mzb.addPlaylist(interaction, client, url)

@tree.command(name = 'aboutthealbum', description = 'display info about a song album')
async def aboutTheAlbum(interaction: discord.Interaction):
    await mzb.aboutTheAlbum(interaction,client)

@tree.command(name = 'abouttheartist', description = 'display info about a song artist')
async def aboutTheAlbum(interaction: discord.Interaction):
    await mzb.aboutTheArtist(interaction,client)

@tree.command(name = 'aboutthesong', description = 'display info about a song')
async def aboutTheSong(interaction: discord.Interaction):
    await mzb.aboutTheSong(interaction,client)

#   dropdown menu for character selection
@tree.command(name = "rp_store", description = "store for rp game")
async def rp_store(interaction: discord.Interaction):
    await botgame.rp_store_gen(interaction)
 #  =======================================

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

 #   create rp for character game
@tree.command(name = "rp_challenge", description = "able to challenge a member  in rp game")
async def rp_challenge_calling(interaction: discord.Interaction):
    await botgame.rp_challenge(interaction)
 #  =======================================

 #  update roles
@tree.command(name = "rp_update_roles", description = "updates everyones roles in server")
async def rp_update_roles(interaction: discord.Interaction):
    await botgame.rp_update_roles_function(interaction)
 #  ===================================================

 #  update roles
@tree.command(name = "rp_schedule", description = "checks up on everyone")
async def rp_schedule(interaction: discord.Interaction):
    await botgame.clearDaily_rpg(interaction, client)
 #  =========================================
 
 #  update roles
@tree.command(name = "rp_fight", description = "enter opponents id to fight")
@app_commands.describe(opp="Please enter opponents ID" )
async def rp_slash_fight(interaction: discord.Interaction, opp: str):
    await botgame.rp_fight_wrapper(interaction, client, opp)
 #  ===========================================
 
#   Shut down Bot safely
@tree.command(name = "shutdown", description = "shuts down the bot SAFELY")
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message(f'Shutting down bot. Goodbye!')
    await client.close()
#   ===================================================

 # calculate simple equation
@tree.command(name = "equation", description= "Simple equation")
@app_commands.describe(simple = "Please enter a simple equation with each spaces in between")
async def equation(interaction: discord.Interaction, simple: str):
    equation = list(simple.split(" "))
    if(reason := calc.simpleCheack(equation)) != True:
        await interaction.response.send_message("The equation sent in not a valid simple equation. Try again.\nReason: " + reason)
    else:
        await interaction.response.send_message(calc.checker(equation))
        
 # calculate algebra equation, needs specification of what to do
@tree.command(name = "algebra", description = "Algebra calculator with several options")
@app_commands.describe(equation = "Please enter an algebra equation with spaces in between", answer = "Enter the following: (slope) - slope intercept form, ")
async def algebra(interaction: discord.Interaction, equation: str, answer: str):
    equation = list(equation.split(" "))
    result = (calc.algebra(equation, answer))
    slope = result[0]
    intercept = result[1]
    await interaction.response.send_message("The slope of the equation is " + str(slope) + ".\nThe y-intercept of the equation is " + str(intercept))


# HELP COMMAND MASTER FUNCTION , PUT ALL COMMAND SPECS HERE
@tree.command(name = 'help', description = 'display information on commands')
async def help(interaction: discord.Interaction):
    await interaction.response.defer()

    await interaction.followup.send("**Discord Bot 320 Master Command Sheet**\n")

    await interaction.followup.send(musicString)
 

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
        
#   give gold
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author != client.user:
        await botgame.rp_message_goldf(message)
        # await message.channel.send('Hello! user id:' + str(message.author.id))
#   =============================================================================

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

# Send Standard Error to Discord Channel
async def errorLogs(message):
    channel = await client.fetch_channel(1094498464710262865)         # Discord Channel Specified Here

    spam = ['rate limited', 'logging in', 'connected to Gateway',     # spam and incorrectly labeled "error messages" in stderr
            'handshake complete','Starting voice','voice...'
            'ffmpeg process', 'should have terminated', 'has not terminated']     

    if any(substring in message for substring in spam ):              # Ignore Spam
        return


    if len(str(message)) < 1900:                                                # Due to discord limitations, need to print description 2000 at a time
        await channel.send(f"**STDERR Output:**\n```\n{str(message)}\n```")     # If less than 1900, send immediately
    else:
        await channel.send(f'**STDERR Output:**\n')
        newerr = ''                                # Else, declare new variable to track 1900 chars at a time
        while len(message) > 1900:                 # Iterate 2000 at a time while geniusLyrics is greater than 2000 **
                    
            newerr = message[:1900]                # string slicing to grab 1900 and send
            await channel.send(f"```\n{str(newerr)}\n```")
            message = message[1900:]               # Error Updated Here                                     **    

        await channel.send(f"\n```\n{str(message)}\n```")

def errhandle(message):
    # Call the async function to send the error message to the Discord channel
    client.loop.create_task(errorLogs(message))
    
sys.stderr.write = errhandle                                        # Standard Error redirection initialized here

client.run(TOKEN)
