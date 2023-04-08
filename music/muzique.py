# shbang
# Started 1/18/2023

# Imports
import os
import asyncio
import discord
from discord.ext import commands
from pydub import AudioSegment
from collections import deque
from discord import app_commands
from dotenv import load_dotenv
import youtube_dl
import ffmpeg
import spotipy
import random
import time
import lyricsgenius
from spotipy.oauth2 import SpotifyClientCredentials

# Loads all the content in the .env folder
load_dotenv() 
TOKEN = os.getenv('DISCORD_API')

# Member list of people in channel to be streamed to (used later)
streaming_members = {}

# YouTube options list set to best audio settings
# Setting options found from youtube-dl documentation
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
yt_params = {'format' :  'bestaudio/best'}
yt_streamObj = youtube_dl.YoutubeDL(yt_params)

# YouTube API Key for gathering metadata
yt_API = os.getenv('YOUTUBE_API')

# Spotify Developer Tokens
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Spotify Client Setup
spotifyCredentials = SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret)
spotifyObj = spotipy.Spotify(client_credentials_manager=spotifyCredentials)

# Genius API for Lyrics Grabbing 
genius_API = os.getenv('GENIUS_API')

# Song List for Queuing
songList = deque()
currentSongUrl = ''
currentSongObj = None


# ** NOTE **
# Class YouTube_linkobj below is borrowed from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py 
# FFMPEG options for seeking found from https://stackoverflow.com/questions/7945747/how-can-you-only-extract-30-seconds-of-audio-using-ffmpeg
#                                       https://stackoverflow.com/questions/65768920/how-to-make-a-discord-music-bot-to-recognize-the-end-of-song-or-where-it-is-play
 #                                      https://stackoverflow.com/questions/69169805/audio-wont-play-on-bot-when-in-a-vc
class YouTube_linkobj(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source)
       
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.songTime = data.get('duration')
        self.songDescription = data.get('description')
        self.uploaderID = data.get('uploader')
        self.uploadDate = data.get('upload_date')
        self.coverArt = data.get('thumbnail')
        self.startTime = 0


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, start=0):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_streamObj.extract_info(url, download=not stream))

        newTime = start
        ff_params = {'options': '-vn', 
                     'before_options': f'-ss {newTime} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        

        if 'entries' in data:
            data = data['entries'][0]                                              # 1st item in playlist index

        filename = data['url'] if stream else yt_streamObj.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ff_params), data=data)       # Return discord.ffmpegpcm audio class 

    # Added this method independently. Used to search YouTube for Spotify Links OR for a general search query (not a link)
    @classmethod
    async def from_search(cls, search, *, loop=None, stream=False, start=0):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_streamObj.extract_info(f"ytsearch:{search}", download=not stream))
        print(f'number of seconds to move is{start}')
        newTime = start
        ff_params = {'options': '-vn', 
                     'before_options': f'-ss {newTime} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

        
        print(f'newtime is {newTime}')
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else yt_streamObj.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ff_params), data=data)


# ================================================================================== Universal / Sys functions

# End Stream | Universal
async def clear(interaction: discord.Interaction):
    await interaction.response.defer()
    server = interaction.guild
    voice_channel = server.voice_client

    if voice_channel is None:
        await interaction.followup.send(f'There is no music to clear!')
    else:
        await voice_channel.disconnect()
        songList.clear()
        await interaction.followup.send(f'Music has been stopped & the queue has been cleared')

# Pause Stream and Unpause Stream | Universal
async def pause_yt(interaction: discord.Interaction):
    await interaction.response.defer()
    vcstatus = interaction.guild.voice_client
    if vcstatus is None:
        await interaction.followup.send('Nothing is currently playing')
    elif vcstatus.is_playing():
        vcstatus.pause()
        await interaction.followup.send('player is now paused')
    elif vcstatus.is_paused():
        vcstatus.resume()
        await interaction.followup.send('player is now un-paused')
    else:
        await interaction.followup.send(f'Unknown error in PAUSE occured')

# Move / Join command | Universal
async def move(interaction: discord.Interaction):    
        await interaction.response.defer()
        try:
            await interaction.followup.send(f'Joining...')                  # Sends attempt message to server
            local = interaction.guild                                               # Create local instances of guild and check for existence of voice client
            voicechan = local.voice_client      
            if voicechan is not None:                                               # Voice channel exists, move to caller's channel
                return await voicechan.move_to(interaction.user.voice.channel)

            await interaction.user.voice.channel.connect()                          # Establish connection after move

        except Exception as err:                                                    # Display general catch-all error for debug purposes
            print(err)

# ============================================================================================================
#
# ================================================================================== Playback Centric Functions

# Play from a link | YouTube , SoundCloud, and Spotify!
async def play(interaction: discord.Interaction, url:str, client: discord.Client):
        await interaction.response.defer() 
        global currentSongUrl
        global currentSongObj
        print("Join being attempted ..")
        local = interaction.guild                                                                   # Establish server context
        voicechan = local.voice_client                                                              # Establish related voice channel
        
        if voicechan is None:                                                                       # If Bot is not in any voice channel, connect
            await interaction.user.voice.channel.connect()
    
        elif interaction.guild.me.voice.channel != interaction.user.voice.channel:                  # Disconnect if the bot is already in a voicechannel
            print("Bot currently not in channel\nJoining...")                                       # That is, a voice channel that's not the user that called the bot
            await local.voice_client.disconnect()
            await interaction.user.voice.channel.connect()

        server = interaction.guild                                                                  # Re-establish server context and voice client after connection
        voice_channel = server.voice_client                                       
        
        print("Before retrieving YouTube Object...")                               
        if (url.startswith('https://open.spotify.com/')) :                                          # Check if Spotify Link
            track_id = url.split('/')[-1]                                                           # Strip '/' and strings after '?'
            head, sep, tail = track_id.partition('?')                                               # So we only have Spotify Song ID
            track_id = head                                                                         # contained in "head" variable
            
            track_info = spotifyObj.track(track_id)                                                 # acquire track info given ID
            track_name = track_info['name']                                                         # Acquire track name, parse for artist names
            track_artists = [artist['name'] for artist in track_info['artists']]                    # In the event of multiple artists
            artistsList = ' '.join(track_artists)
            final = track_name + " by " + artistsList                                               # Join Title and Artists and perform YT search query
            filename = await YouTube_linkobj.from_search(final, loop=client.loop, stream=True, start=0)

                                                                                                    # Check if YouTube or Soundcloud Link
                                                                                                    # Note: YouTube_linkobj shares functionality
                                                                                                    #       with both YouTube and SoundCloud links
                                                                                                    #       So we can share logic here 
        elif ((url.startswith('https://www.youtube.com/')) or url.startswith('https://soundcloud.com/') ):   
            print("Link...")
            filename = await YouTube_linkobj.from_url(url, loop=client.loop, stream=True, start=0)
        
        else:                                                                                       # Else, perform General Search Query (YouTube)
            print("Search...")
            filename = await YouTube_linkobj.from_search(url, loop=client.loop, stream=True, start=0)

        print("Before Playing in channel...")
        if voice_channel.is_playing():                                                              # If the bot is playing, add song to a queue
            songList.append(filename)
            await interaction.followup.send(f'Added {filename.title} to queue')             # Send user friendly message

        else:                                                                                       # Else, begin playing the next song
            voice_channel.play(filename, after=lambda next: nextSong(interaction, client))          # Upon .play operation ending, after uses lambda function next
            print("Before user-end interaction message...")                                         # Calls upon nextSong given interaction and client to loop through queue
            currentSongUrl = filename.title
            currentSongObj = filename
            await interaction.followup.send(f'Now playing {filename.title}')                # Happens for every song until queue is empty

        #print("Reached here in command")      
        #print("Song Lists and URLS in PLAY command")
        #print(songList)                                    

# Supplementary Queuing and Loop function to be used in tandem with 'play' command
# Note: NOT TREE FUNCTION ACCESSIBLE
def nextSong(interaction: discord.Interaction, client: discord.Client):                             # Feed discord Interaction and client objects
    print("NEXT SONG REACHED")
    if len(songList) > 0:                                                                           # SongList is not empty
        localsong = songList.popleft()                                                              # Acquire first song in queue
        local = interaction.guild                                                                   # Establish server context
        voicechan = local.voice_client  

        
        logChannel = client.get_channel(1084674930060312576)                                        # Establish Channel for logging non-response messages        
        #print("Before logchannel")                                                                 # Debug Prints
        send = logChannel.send(f'Now playing {localsong.title}')                                    # Send message upon new song to log channel within server
        #print("After logchannel")                                                                   
        asyncio.run_coroutine_threadsafe(send, client.loop)                                         # Use asyncio.run_coroutine_threadsafe to run message command from synchronous function
        voicechan.play(localsong, after=lambda next: nextSong(interaction, client))                 # Play and recursively call upon nextSong while songList is not empty
        
        global currentSongUrl
        global currentSongObj
        currentSongUrl = localsong.title
        currentSongObj = localsong

        # Dev Note: Have to use asyncio.run_coroutine_threadsafe as song is playing in a separate async function
        #           Need to access interaction from function while song is playing. Causes weird bugs if not used.
        #           Traceback error 4006 upon too many queue entries. Need threadSafe to access and loop safely.
        #           ** REMEMBER FOR ALL FURTHER FUNCTIONS ACCESSING FROM ASYNC FUNCTION ** 

        # Professor Note: Used sources to familiarize with asyncio.run_coroutine_threadsafe:
        #                 https://docs.python.org/3/library/asyncio-task.html#scheduling-from-other-threads

    else:                                                                                           # No songs in queue, disconnect
        asyncio.run_coroutine_threadsafe(interaction.guild.voice_client.disconnect(), client.loop)
        currentSongUrl=''
        currentSongObj = None

    print("NEXT SONG COMPLETE")

# Skipping songs function
async def skipSong(interaction: discord.Interaction, client: discord.Client):
    #print("Before Skip")                                                                       # Debug Prints
    await interaction.response.defer()
    print(songList)
    local = interaction.guild                                                                   # Establish server context
    voicechan = local.voice_client                                                              # Establish related voice channel

    if voicechan is None:
        await interaction.followup.send(f'No current song playing to skip!')
    elif voicechan.is_playing():
        await interaction.followup.send(f'Skipping song')
        voicechan.stop()
    else:
        await interaction.followup.send(f'Unknown error in SKIP occured')
    #print("After Skip") 
    #print(songList)

# Displays the current queue of songs to be played
async def displayQueue(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if len(songList) != 0:                                                           
        await interaction.followup.send(f'Current Queue is:')
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        i = 1
        for songs in songList:
            display = songs.title
            display = str(i) + ": " + display
            await logChannel.send(display)
            i = i+1
    else: 
        await interaction.followup.send(f'No active Queue to be displayed!')

# Shuffles the Current Queue of Songs and Redisplays it
async def shuffleQueue(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if len(songList) != 0:
        await interaction.followup.send(f'Queue Shuffled. Current Queue is now:')

        random.shuffle(songList)
        
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        i = 1
        for songs in songList:
            display = songs.title
            display = str(i) + ": " + display
            await logChannel.send(display)
            i = i+1
    else:
        await interaction.followup.send(f'No active Queue to be shuffled!')


# Shifting The Track
async def fastForwardSong(interaction: discord.Interaction, client: discord.Client, seconds: int):
    await interaction.response.defer()
    local = interaction.guild                                                                   # Establish server context
    voicechan = local.voice_client   
    #global currentSongTime
    print("CURRNET SONG LISTS ARE")
    print(songList)
    print("Reached Fast Forward")                                                          # Establish related voice channel
    if currentSongUrl !='':                               # NOte: ADD condition for Song Obj existing here, else display error                          
        print("If condition met in Fast forward")
        if (seconds > 0) and (seconds < currentSongObj.songTime):
            #currentSongTime = ((time.time()) - currentSongTime) + seconds
            print("Before retrieving YouTube Object...")    
            print("Song Urls Before Appending")   

            # current song url update        
   
            print(f'Updated var is {currentSongUrl}')          
            if (currentSongUrl.startswith('https://open.spotify.com/')) :                               # Check if Spotify Link
                track_id = currentSongUrl.split('/')[-1]                                                # Strip '/' and strings after '?'
                head, sep, tail = track_id.partition('?')                                               # So we only have Spotify Song ID
                track_id = head                                                                         # contained in "head" variable
                
                track_info = spotifyObj.track(track_id)                                                 # acquire track info given ID
                track_name = track_info['name']                                                         # Acquire track name, parse for artist names
                track_artists = [artist['name'] for artist in track_info['artists']]                    # In the event of multiple artists
                artistsList = ' '.join(track_artists)
                final = track_name + " by " + artistsList                                               # Join Title and Artists and perform YT search query
                filename = await YouTube_linkobj.from_search(final, loop=client.loop, stream=True, start=seconds)

                                                                                                        # Check if YouTube or Soundcloud Link
                                                                                                        # Note: YouTube_linkobj shares functionality
                                                                                                        #       with both YouTube and SoundCloud links
                                                                                                        #       So we can share logic here 
            elif ((currentSongUrl.startswith('https://www.youtube.com/')) or currentSongUrl.startswith('https://soundcloud.com/') ):   
                print("Link...")
                filename = await YouTube_linkobj.from_url(currentSongUrl, loop=client.loop, stream=True, start=seconds)
            
            else:                                                                                       # Else, perform General Search Query (YouTube)
                print("Search...")
                filename = await YouTube_linkobj.from_search(currentSongUrl, loop=client.loop, stream=True, start=seconds)

            songList.appendleft(filename)
            print("SONGLISTS after are")
            print(songList)
            voicechan.stop()
            print("Music stopped. New fast forward song added")
            #currentSongTime = time.time()
            print("Time reset in Fast forward")
            await interaction.followup.send(f'Shifting Track to {seconds} seconds...')
        
        else:
            await interaction.followup.send(
                f'Invalid Number of Seconds Entered (check that the value is not 0, and the seconds does not exceed the duration of the song)') 


# Repeating a track
async def encore(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    global currentSongObj
    if currentSongObj != None and currentSongUrl!= '':
        print("Passed if in encore")
        if (currentSongUrl.startswith('https://open.spotify.com/')) :                               # Check if Spotify Link
                track_id = currentSongUrl.split('/')[-1]                                                # Strip '/' and strings after '?'
                head, sep, tail = track_id.partition('?')                                               # So we only have Spotify Song ID
                track_id = head                                                                         # contained in "head" variable
                
                track_info = spotifyObj.track(track_id)                                                 # acquire track info given ID
                track_name = track_info['name']                                                         # Acquire track name, parse for artist names
                track_artists = [artist['name'] for artist in track_info['artists']]                    # In the event of multiple artists
                artistsList = ' '.join(track_artists)
                final = track_name + " by " + artistsList                                               # Join Title and Artists and perform YT search query
                filename = await YouTube_linkobj.from_search(final, loop=client.loop, stream=True, start=0)

                                                                                                        # Check if YouTube or Soundcloud Link
                                                                                                        # Note: YouTube_linkobj shares functionality
                                                                                                        #       with both YouTube and SoundCloud links
                                                                                                        #       So we can share logic here 
        elif ((currentSongUrl.startswith('https://www.youtube.com/')) or currentSongUrl.startswith('https://soundcloud.com/') ):   
                print("Link...")
                filename = await YouTube_linkobj.from_url(currentSongUrl, loop=client.loop, stream=True, start=0)
            
        else:                                                                                       # Else, perform General Search Query (YouTube)
                print("Search...")
                filename = await YouTube_linkobj.from_search(currentSongUrl, loop=client.loop, stream=True, start=0)
        
        songList.appendleft(filename)                                                               # Append new YouTube obj to top of the list
        await interaction.followup.send(f'{currentSongObj.title} queued for repeat ')
    else:
        await interaction.followup.send(' No song is currently playing to repeat! ')

# Shift Two Song's indexes
async def swap(interaction: discord.Interaction, client: discord.Client, indexone: int, indextwo: int):
    await interaction.response.defer()
    if (len(songList) > 1) and indexone !=0 and indextwo !=0:
        songList[indexone-1], songList[indextwo-1] = songList[indextwo-1], songList[indexone-1]
        await interaction.followup.send(f'Index {indexone} and Index {indextwo} are now swapped! Current Index is now:')

        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        i = 1
        for songs in songList:
            display = songs.title
            display = str(i) + ": " + display
            await logChannel.send(display)
            i = i+1
    
    else:
        await interaction.followup.send(' Queue is not large enough to swap anything! Or you have entered 0 for one of the indexes ')

# Display Song Info
async def displayInfo(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if currentSongObj != None:
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)

        calendar = ['January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August',
                    'September', 'October', 'November', 'December']
        
        uploadYear = processYear(currentSongObj.uploadDate)
        uploadMonth = processMonth(currentSongObj.uploadDate)
        uploadDay = processDay(currentSongObj.uploadDate)

        if uploadMonth == '01':
            uploadMonth = calendar[0]
        elif uploadMonth == '02':
            uploadMonth = calendar[1]
        elif uploadMonth == '03':
            uploadMonth = calendar[2]
        elif uploadMonth == '04':
            uploadMonth = calendar[3]
        elif uploadMonth == '05':
            uploadMonth = calendar[4]
        elif uploadMonth == '06':
            uploadMonth = calendar[5]
        elif uploadMonth == '07':
            uploadMonth = calendar[6]
        elif uploadMonth == '08':
            uploadMonth = calendar[7]
        elif uploadMonth == '09':
            uploadMonth = calendar[8]
        elif uploadMonth == '10':
            uploadMonth = calendar[9]
        elif uploadMonth == '11':
            uploadMonth = calendar[10]
        elif uploadMonth == '12':
            uploadMonth = calendar[11]

        totalMinutes = int(currentSongObj.songTime/60)
        totalSeconds = currentSongObj.songTime % 60

        await interaction.followup.send('Current Song Information:')
        await logChannel.send(f'1. Title: {currentSongObj.title}')
        await logChannel.send(f'2. Song Duration: {totalMinutes} minutes, {totalSeconds} seconds')
        await logChannel.send(f'3. Uploader: {currentSongObj.uploaderID}')
        await logChannel.send(f'4. Upload Date: {uploadMonth} {uploadDay}, {uploadYear}')
        await logChannel.send(f'5. Cover Art: {currentSongObj.coverArt}')
        await logChannel.send(f'6. Description: {currentSongObj.songDescription}')
    else:
        await interaction.followup.send('No song is currently playing to display information for!')


# Display Lyrics for a given song
async def displayLyrics(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if currentSongObj is None:
        await interaction.followup.send('There is no currently playing song to display lyrics for')
    else:
        print("First lyrics condition met")
        print(currentSongObj.title)                                 # Acquire current song title (likely from youtube unless its from soundcloud)
        geniusClient = lyricsgenius.Genius(genius_API)              # Establish Genius client with API key from .env
        filteredTitle = currentSongObj.title                        # New Title variable for filtering stylist title stuff like '[' and '(' 
        
        print(filteredTitle)                                        # Debug Prints scattered for Dev for tracing errors
        print(type(filteredTitle))
        
        finalTitle = filterTitle(filteredTitle)
        
        geniusSong = geniusClient.search_song(title = finalTitle)   # Search with new filtered title ** Note: THIS IS NOT PERFECTLY WORKING, GENIUS API SEARCH IS NOT STELLAR ** 
        logId = interaction.channel_id                                  # Channel ID acquisition to send lyrics to
        logChannel = client.get_channel(logId)
        print("Lyrics search has been conducted")

        if geniusSong is not None:                                  # song has been found from Genius website
            print("Second lyrics condition met")
            await interaction.followup.send('Lyrics for this song have been found:')
            print({geniusSong.lyrics})
            geniusLyrics = geniusSong.lyrics

            if len(geniusLyrics) < 2000:                            # Due to discord limitations, need to print lyrics 2000 at a time
                await logChannel.send(geniusLyrics)                 # If less than 2000, send immediately
            else:
                newLyrics = ''                                      # Else, declare new variable to track 2000 chars at a tim
                while len(geniusLyrics) > 2000:                     # Iterate 2000 at a time while geniusLyrics is greater than 2000 **
                    
                    newLyrics = geniusLyrics[:2000]                 # string slicing to grab 2000 and send
                    await logChannel.send(newLyrics)
                    geniusLyrics = geniusLyrics[2000:]              # genius lyrics updated here                                     **
            
            
            await logChannel.send(geniusLyrics)                     # Send remainder of lyrics
            
        
        else:
            await interaction.followup.send('Lyrics for this song could not be found')



def filterTitle(filteredTitle:str):
        # https://www.w3schools.com/python/ref_string_strip.asp     Strip method for whitespaces found here
        filteredTitle1 = filteredTitle.split('[')[0]                 # Filter stylistic things from title
        filteredTitle2 = filteredTitle1.split('(')[0]
        filteredTitle3 = filteredTitle2.split('ft')[0]
        filteredTitle4 = filteredTitle3.split('ft.')[0]
        filteredTitle5 = filteredTitle4.split('feat.')[0]
        filteredTitle6 = filteredTitle5.split('feat')[0]
        filteredTitle7 = filteredTitle6.split('featuring')[0]
        return filteredTitle7


def processMonth(garbledStr:str):
        calendar = ['January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August',
                    'September', 'October', 'November', 'December']
        
        uploadMonth = garbledStr[4:6]

        if uploadMonth == '01':
            uploadMonth = calendar[0]
        elif uploadMonth == '02':
            uploadMonth = calendar[1]
        elif uploadMonth == '03':
            uploadMonth = calendar[2]
        elif uploadMonth == '04':
            uploadMonth = calendar[3]
        elif uploadMonth == '05':
            uploadMonth = calendar[4]
        elif uploadMonth == '06':
            uploadMonth = calendar[5]
        elif uploadMonth == '07':
            uploadMonth = calendar[6]
        elif uploadMonth == '08':
            uploadMonth = calendar[7]
        elif uploadMonth == '09':
            uploadMonth = calendar[8]
        elif uploadMonth == '10':
            uploadMonth = calendar[9]
        elif uploadMonth == '11':
            uploadMonth = calendar[10]
        elif uploadMonth == '12':
            uploadMonth = calendar[11]

        return uploadMonth

def processDay(garbledStr:str):
    uploadDay = garbledStr[6:]
    return uploadDay

def processYear(garbledStr:str):
    uploadYear = garbledStr[:4]
    return uploadYear





# ============================================================================================================

