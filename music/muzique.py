# shbang
# Started 1/18/2023

# Imports
import os
import sys
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
import wikipediaapi
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

yt_playlistParams = {'extract_flat': 'in_playlist', 'format': 'bestaudio/best'}
yt_playlistObj = youtube_dl.YoutubeDL(yt_playlistParams)

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

# Music Strings for Help Command
# Initialize once outside of function
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


# ** NOTE **
# Class YouTube_linkobj below is borrowed from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py 
# FFMPEG options for seeking found from https://stackoverflow.com/questions/7945747/how-can-you-only-extract-30-seconds-of-audio-using-ffmpeg
#                                       https://stackoverflow.com/questions/65768920/how-to-make-a-discord-music-bot-to-recognize-the-end-of-song-or-where-it-is-play
 #                                      https://stackoverflow.com/questions/69169805/audio-wont-play-on-bot-when-in-a-vc
class YouTube_linkobj(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source)
                                        # Declare Music data fields for songs that can be acquired
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
    
    # Added this method independently. Used to search for Playlists and gets song data and title one by one
    # Note: Returns list of songs, audio objects not playable. Need to use titles and call upon from_search or from_link in class
    @classmethod
    async def yt_playlist(cls, url, *, loop=None, stream=False, start=0):
        loop = loop or asyncio.get_event_loop()
        
    
        data = await loop.run_in_executor(None, lambda: yt_playlistObj.extract_info(url, download=not stream))
        
        entries = data.get('entries')

        newTime = start
        ff_params = {'options': '-vn', 
                     'before_options': f'-ss {newTime} -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        
        classlist = []
        for entry in entries:
            filename = entry['url'] if stream else youtube_dl.prepare_filename(entry)
            classlist.append(cls(discord.FFmpegPCMAudio(filename, **ff_params), data=entry))

        return classlist


# ================================================================================== Universal / Sys functions

# End Stream | Universal
async def clear(interaction: discord.Interaction):
    await interaction.response.defer()
    server = interaction.guild
    voice_channel = server.voice_client
                                                                            # Check that voice_cleint is established
    if voice_channel is None:
        await interaction.followup.send(f'There is no music to clear!')
    else:
        await voice_channel.disconnect()                                    # If so, Leave voice channel and clear queue
        songList.clear()
        await interaction.followup.send(f'Music has been stopped & the queue has been cleared')

# Pause Stream and Unpause Stream | Universal
async def pause_yt(interaction: discord.Interaction):
    await interaction.response.defer()
    vcstatus = interaction.guild.voice_client
                                                                            # Check voice_client is established, if so: pause
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
            print(f"{err}", file=sys.stderr)                                        # Display to Standard Error for our error log channel
            await interaction.followup.send(f'User is not in a voice channel!')

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
        
        caller = interaction.user
        callerID = interaction.guild.get_member(caller.id)

        voicecheck = getattr(callerID, 'voice', None)
        channelcheck = getattr(voicecheck, 'channel', None)


        if channelcheck is None:
            await interaction.followup.send(f'User is not in a voice channel!')

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

    if voicechan is None:                                                                       # Check song exists
        await interaction.followup.send(f'No current song playing to skip!')
    elif voicechan.is_playing():
        await interaction.followup.send(f'Skipping song')
        voicechan.stop()                                                                        # If it does, stop song, nextSong called
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

        # Use python Value swap format (x,y = y,x) to swap index values
        songList[indexone-1], songList[indextwo-1] = songList[indextwo-1], songList[indexone-1]
        await interaction.followup.send(f'Index {indexone} and Index {indextwo} are now swapped! Current Index is now:')
        

        # Send Updated Queue Here
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
        
        # Process Date using Commands below
        uploadYear = processYear(currentSongObj.uploadDate)
        uploadMonth = processMonth(currentSongObj.uploadDate)
        uploadDay = processDay(currentSongObj.uploadDate)

        # Month cases here
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

        # Change seconds to minutes, grab remaining seconds after minutes 
        totalMinutes = int(currentSongObj.songTime/60)
        totalSeconds = currentSongObj.songTime % 60

        # Begin sending Info here
        await interaction.followup.send('Current Song Information:')
        await logChannel.send(f'1. Title: {currentSongObj.title}')
        await logChannel.send(f'2. Song Duration: {totalMinutes} minutes, {totalSeconds} seconds')
        await logChannel.send(f'3. Uploader: {currentSongObj.uploaderID}')
        await logChannel.send(f'4. Upload Date: {uploadMonth} {uploadDay}, {uploadYear}')
        await logChannel.send(f'5. Cover Art: {currentSongObj.coverArt}')
        #await logChannel.send(f'6. Description: {currentSongObj.songDescription}')

        desc = currentSongObj.songDescription
        if len(desc) < 2000:                                      # Due to discord limitations, need to print description 2000 at a time
            await logChannel.send(f'6. Description: {desc}')      # If less than 2000, send immediately
        else:
            await logChannel.send(f'6. Description: ')
            newdesc = ''                                # Else, declare new variable to track 2000 chars at a time
            while len(desc) > 2000:                     # Iterate 2000 at a time while geniusLyrics is greater than 2000 **
                    
                newdesc = desc[:2000]                   # string slicing to grab 2000 and send
                await logChannel.send(newdesc)
                desc = desc[2000:]                      # YT description updated here                                     **
            
            
            await logChannel.send(desc)                 # Send remainder of description

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
        logId = interaction.channel_id                              # Channel ID acquisition to send lyrics to
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
            
            
                await logChannel.send(geniusLyrics)                 # Send remainder of lyrics
            
        
        else:
            await interaction.followup.send('Lyrics for this song could not be found')


# Filter title from typical youtube Styling things
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

# Slice string for the month, return Month name (not numbers)
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

# Slice String to Acquire Day
def processDay(garbledStr:str):
    uploadDay = garbledStr[6:]
    return uploadDay

# Slice String to acquire year 
def processYear(garbledStr:str):
    uploadYear = garbledStr[:4]
    return uploadYear


# Shuffles the Current Queue of Songs and Redisplays it
async def shuffleQueue(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if len(songList) != 0:                                                              # Check that Song list is not empty
        await interaction.followup.send(f'Queue Shuffled. Current Queue is now:')

        random.shuffle(songList)                                                        # call upon random.shuffle for easy dequeue shuffling
        
        logId = interaction.channel_id                                                  # Get interaction Channel
        logChannel = client.get_channel(logId)
        i = 1
        for songs in songList:                                                          # Begin sending songs and updated queue to channel
            display = songs.title
            display = str(i) + ": " + display
            await logChannel.send(display)
            i = i+1
    else:
        await interaction.followup.send(f'No active Queue to be shuffled!')


# Shifting The Track
# Convenient for shifting when you don't know the exact time in seconds
# but you're thinking "Oh hey, that part halfway in the song was pretty good, lets go to that part"
async def percentageShift(interaction: discord.Interaction, client: discord.Client, percent: int):
    await interaction.response.defer()
    local = interaction.guild                                                                  # Establish server context
    voicechan = local.voice_client   

    print("CURRENT SONG LISTS ARE")
    print(songList)
    print("Reached Shift Percentage")                                                          # Establish related voice channel

                                                                                               # Percentage Cases , 0 is 0, calculate for rest, 100 skips song
    if (percent == 0):                                                                         
        seconds = 0

    elif (percent == 1):
        seconds = (0.01 * currentSongObj.songTime)
    
    elif (percent == 2):
        seconds = (0.02 * currentSongObj.songTime)

    elif (percent == 3):
        seconds = (0.03 * currentSongObj.songTime)
    
    elif (percent == 4):
        seconds = (0.04 * currentSongObj.songTime)

    elif (percent == 5):
        seconds = (0.05 * currentSongObj.songTime)

    elif (percent == 6):
        seconds = (0.06 * currentSongObj.songTime)

    elif (percent == 7):
        seconds = (0.07 * currentSongObj.songTime)

    elif (percent == 8):
        seconds = (0.08 * currentSongObj.songTime)

    elif (percent == 9):
        seconds = (0.09 * currentSongObj.songTime)

    elif (percent == 10):
        seconds = (0.10 * currentSongObj.songTime)

    elif (percent == 11):
        seconds = (0.11 * currentSongObj.songTime)

    elif (percent == 12):
        seconds = (0.12 * currentSongObj.songTime)

    elif (percent == 13):
        seconds = (0.13 * currentSongObj.songTime)

    elif (percent == 14):
        seconds = (0.14 * currentSongObj.songTime)

    elif (percent == 15):
        seconds = (0.15 * currentSongObj.songTime)

    elif (percent == 16):
        seconds = (0.16 * currentSongObj.songTime)

    elif (percent == 17):
        seconds = (0.17 * currentSongObj.songTime)

    elif (percent == 18):
        seconds = (0.18 * currentSongObj.songTime)

    elif (percent == 19):
        seconds = (0.19 * currentSongObj.songTime)

    elif (percent == 20):
        seconds = (0.20 * currentSongObj.songTime)

    elif (percent == 21):
        seconds = (0.21 * currentSongObj.songTime)

    elif (percent == 22):
        seconds = (0.22 * currentSongObj.songTime)

    elif (percent == 23):
        seconds = (0.23 * currentSongObj.songTime)

    elif (percent == 24):
        seconds = (0.24 * currentSongObj.songTime)

    elif (percent == 25):
        seconds = (0.25 * currentSongObj.songTime)

    elif (percent == 26):
        seconds = (0.26 * currentSongObj.songTime)

    elif (percent == 27):
        seconds = (0.27 * currentSongObj.songTime)

    elif (percent == 28):
        seconds = (0.28 * currentSongObj.songTime)

    elif (percent == 29):
        seconds = (0.29 * currentSongObj.songTime)

    elif (percent == 30):
        seconds = (0.30 * currentSongObj.songTime)

    elif (percent == 31):
        seconds = (0.31 * currentSongObj.songTime)

    elif (percent == 32):
        seconds = (0.32 * currentSongObj.songTime)

    elif (percent == 33):
        seconds = (0.33 * currentSongObj.songTime)

    elif (percent == 34):
        seconds = (0.34 * currentSongObj.songTime)

    elif (percent == 35):
        seconds = (0.35 * currentSongObj.songTime)

    elif (percent == 36):
        seconds = (0.36 * currentSongObj.songTime)

    elif (percent == 37):
        seconds = (0.37 * currentSongObj.songTime)

    elif (percent == 38):
        seconds = (0.38 * currentSongObj.songTime)

    elif (percent == 39):
        seconds = (0.39 * currentSongObj.songTime)

    elif (percent == 40):
        seconds = (0.40 * currentSongObj.songTime)

    elif (percent == 41):
        seconds = (0.41 * currentSongObj.songTime)

    elif (percent == 42):
        seconds = (0.42 * currentSongObj.songTime)

    elif (percent == 43):
        seconds = (0.43 * currentSongObj.songTime)

    elif (percent == 44):
        seconds = (0.44 * currentSongObj.songTime)

    elif (percent == 45):
        seconds = (0.45 * currentSongObj.songTime)

    elif (percent == 46):
        seconds = (0.46 * currentSongObj.songTime)

    elif (percent == 47):
        seconds = (0.47 * currentSongObj.songTime)

    elif (percent == 48):
        seconds = (0.48 * currentSongObj.songTime)

    elif (percent == 49):
        seconds = (0.49 * currentSongObj.songTime)

    elif (percent == 50):
        seconds = (0.50 * currentSongObj.songTime)

    elif (percent == 51):
        seconds = (0.51 * currentSongObj.songTime)

    elif (percent == 52):
        seconds = (0.52 * currentSongObj.songTime)

    elif (percent == 53):
        seconds = (0.53 * currentSongObj.songTime)

    elif (percent == 54):
        seconds = (0.54 * currentSongObj.songTime)

    elif (percent == 55):
        seconds = (0.55 * currentSongObj.songTime)

    elif (percent == 56):
        seconds = (0.56 * currentSongObj.songTime)

    elif (percent == 57):
        seconds = (0.57 * currentSongObj.songTime)

    elif (percent == 58):
        seconds = (0.58 * currentSongObj.songTime)

    elif (percent == 59):
        seconds = (0.59 * currentSongObj.songTime)

    elif (percent == 60):
        seconds = (0.60 * currentSongObj.songTime)

    elif (percent == 61):
        seconds = (0.61 * currentSongObj.songTime)

    elif (percent == 62):
        seconds = (0.62 * currentSongObj.songTime)

    elif (percent == 63):
        seconds = (0.63 * currentSongObj.songTime)

    elif (percent == 64):
        seconds = (0.64 * currentSongObj.songTime)

    elif (percent == 65):
        seconds = (0.65 * currentSongObj.songTime)

    elif (percent == 66):
        seconds = (0.66 * currentSongObj.songTime)

    elif (percent == 67):
        seconds = (0.67 * currentSongObj.songTime)

    elif (percent == 68):
        seconds = (0.68 * currentSongObj.songTime)

    elif (percent == 69):
        seconds = (0.69 * currentSongObj.songTime)

    elif (percent == 70):
        seconds = (0.70 * currentSongObj.songTime)

    elif (percent == 71):
        seconds = (0.71 * currentSongObj.songTime)

    elif (percent == 72):
        seconds = (0.72 * currentSongObj.songTime)

    elif (percent == 73):
        seconds = (0.73 * currentSongObj.songTime)

    elif (percent == 74):
        seconds = (0.74 * currentSongObj.songTime)

    elif (percent == 75):
        seconds = (0.75 * currentSongObj.songTime)

    elif (percent == 76):
        seconds = (0.76 * currentSongObj.songTime)

    elif (percent == 77):
        seconds = (0.77 * currentSongObj.songTime)

    elif (percent == 78):
        seconds = (0.78 * currentSongObj.songTime)

    elif (percent == 79):
        seconds = (0.79 * currentSongObj.songTime)

    elif (percent == 80):
        seconds = (0.80 * currentSongObj.songTime)

    elif (percent == 81):
        seconds = (0.81 * currentSongObj.songTime)

    elif (percent == 82):
        seconds = (0.82 * currentSongObj.songTime)

    elif (percent == 83):
        seconds = (0.83 * currentSongObj.songTime)

    elif (percent == 84):
        seconds = (0.84 * currentSongObj.songTime)

    elif (percent == 85):
        seconds = (0.85 * currentSongObj.songTime)

    elif (percent == 86):
        seconds = (0.86 * currentSongObj.songTime)

    elif (percent == 87):
        seconds = (0.87 * currentSongObj.songTime)

    elif (percent == 88):
        seconds = (0.88 * currentSongObj.songTime)

    elif (percent == 89):
        seconds = (0.89 * currentSongObj.songTime)

    elif (percent == 90):
        seconds = (0.90 * currentSongObj.songTime)

    elif (percent == 91):
        seconds = (0.91 * currentSongObj.songTime)

    elif (percent == 92):
        seconds = (0.92 * currentSongObj.songTime)

    elif (percent == 93):
        seconds = (0.93 * currentSongObj.songTime)

    elif (percent == 94):
        seconds = (0.94 * currentSongObj.songTime)

    elif (percent == 95):
        seconds = (0.95 * currentSongObj.songTime)

    elif (percent == 96):
        seconds = (0.96 * currentSongObj.songTime)

    elif (percent == 97):
        seconds = (0.97 * currentSongObj.songTime)

    elif (percent == 98):
        seconds = (0.98 * currentSongObj.songTime)

    elif (percent == 99):
        seconds = (0.99 * currentSongObj.songTime)
    
    elif (percent == 100):                                                                              # Skip song in 100 case
        voicechan.stop()
        await interaction.followup.send(f'100% Entered. Skipping song...')

    else:
        await interaction.followup.send(f'Invalid Percentage Value entered!')                           # Debug Interaction


    # =================================================================== # 
    seconds = int(seconds)
    if currentSongUrl !='':                                                                             # Song needs to exist before continuing             
        print("If condition met in Fast forward")
        if (seconds < currentSongObj.songTime):
            print("Before retrieving YouTube Object...")    
            print("Song Urls Before Appending")   

            # Update Current Song URL        
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
            print("Time reset in Shift")
            await interaction.followup.send(f'Shifting Track to {percent}% of total runtime ({seconds} seconds)')
        
        else:
            await interaction.followup.send(
                f'Unknown Error in PERCENTAGE SHIFT occurred (this should not happen)') 


async def addPlaylist(interaction: discord.Interaction, client: discord.Client, url: str):

    # Note: Bot NEEDS to be playing at least one song already before adding playlist or it will turn into a buggy mess
    # Add check on next commit, need thorough testing
    await interaction.response.defer()

    # Song needs to be playing before adding a song to playlist
    if (currentSongObj is not None):

        # Begin Search here if a valid playlist link is given
        # List returned to local list with song names in playlist
        if ((url.startswith('https://www.youtube.com/playlist'))):
            locallist = await YouTube_linkobj.yt_playlist(url, loop=client.loop, stream=True, start=0)

            # Debug
            print(locallist)
            print("Local list received. Iterating now")

            # Call Upon youtube Link acquisition function for each item in the list
            for items in locallist:
                playlistsong = await YouTube_linkobj.from_url(items.url, loop=client.loop, stream=True, start=0)
                songList.append(playlistsong)                                # Append to main song List / queue

            await interaction.followup.send("Playlist added to queue")
        else:
            await interaction.followup.send("Invalid Playlist link")
    
    else:
        await interaction.followup.send("Need to have at least one song playing before adding queue!")



# About the Song
async def aboutTheSong(interaction: discord.Interaction, client: discord.Client):
    await interaction.response.defer()
    if currentSongObj is None:
        await interaction.followup.send("Can't gather information from current song. No song is playing!")

                                                                        # Song is playing, get interaction channel to send there
    else:
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        titleToSearch = currentSongObj.title

                                                                        # Begin Spotify Query, get Track title, artist, and album name
        searchResults = spotifyObj.search(q=titleToSearch, type="track")
        songTrack = searchResults["tracks"]["items"][0]["name"]
        songTrackArtist = searchResults["tracks"]["items"][0]["artists"][0]["name"]
        songAlbum = searchResults["tracks"]["items"][0]["album"]["name"]

        wikiInit = wikipediaapi.Wikipedia('en')
        albumPage = wikiInit.page(songTrack)
        #displayPage = albumPage.summary
        
                                                                        # Set Flag, begin iterating categories in page
        found_link = False
        if albumPage.exists():
            for cats in albumPage.categories:                           # secondary check follows IF disambiguation page
                if "disambiguation pages" in cats or "Disambiguation pages" in cats:
                    print("IN DISAMBIG PAGE\n")
                    links = albumPage.links
                    for link in links:                                  # Check if links in disambiguation page match artist title
                        if ("song" and songTrack.lower() and songTrackArtist.lower()) in link.lower():
                            print(link.lower())
                            print("HIT SONG")
                            albumPage = wikiInit.page(link)
                            print("HIT LINK")
                            found_link = True                           # If so, set flag and break
                            break
                if found_link:
                    break
            displayPage = albumPage.summary                             # Update Wikipedia Page here if needed
        else:
            displayPage = "No Song Information found"
        
        # Begin sending Info here
        await interaction.followup.send("Information Found!")
        await logChannel.send(f"1. Track Name is {songTrack}")
        await logChannel.send(f"2. Artist Name is {songTrackArtist}")
        await logChannel.send(f"3. Album Name is {songAlbum}")

        if len(displayPage) < 2000:                                     # Due to discord limitations, need to print description 2000 at a time
            await logChannel.send(f'4. Description: {displayPage}')     # If less than 2000, send immediately
        else:
            await logChannel.send(f'4. Description: ')
            newdisplay = ''                                             # Else, declare new variable to track 2000 chars at a time
            while len(displayPage) > 2000:                              # Iterate 2000 at a time 
                    
                newdisplay = displayPage[:2000]                         # string slicing to grab 2000 and send
                await logChannel.send(newdisplay)
                displayPage = displayPage[2000:]                        # YT description updated here          
            
            
            await logChannel.send(displayPage)                          # Send remainder of description



# About the Album
async def aboutTheAlbum(interaction: discord.Interaction, client: discord.Client):
    
    await interaction.response.defer()
    if currentSongObj is None:
        await interaction.followup.send("Can't gather information from current song. No song is playing!")

    else:
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)                          # Send data to channel interaction was called from
        
                                                                        # Search Spotify DB for track title and grab first
        songSearchFirst = spotifyObj.search(q=currentSongObj.title, type="track")
        songTrack = songSearchFirst["tracks"]["items"][0]

                                                                        # Grab the first album name from search
        titleToSearch = songTrack["album"]["name"]                  

        searchResults = spotifyObj.search(q=titleToSearch, type="album")# Return Spotify search query to search Results

        if searchResults == {}:
            await interaction.followup.send("Error with Spotify Link Search: No Albums could be found")
            return

                                                                        # acquire album name from searchResults spotify object and get album object
        albumSearch = searchResults["albums"]["items"][0]["external_urls"]["spotify"]
        albumDetails = spotifyObj.album(albumSearch)

        if "error" in albumDetails:
            await interaction.followup.send("Error with Spotify Album Search: Album ID nonexistent")
            return

        albumName = albumDetails["name"]    
        print(albumDetails)                     # Debug


                                                                        # Begin wikipedia initialization, get page from name
        wikiInit = wikipediaapi.Wikipedia('en')
        albumPage = wikiInit.page(albumName)
        #displayPage = albumPage.summary
        
        found_link = False                                              # Custom flag for exiting disambig. page
        if albumPage.exists():
            for cats in albumPage.categories:                           # Iterate categories in Wikipedia page, if dsiambig. search for title
                if "disambiguation pages" in cats or "Disambiguation pages" in cats:
                    print("IN DISAMBIG PAGE\n")
                    links = albumPage.links
                    for link in links:                                  # In this field, if title is found, change wiki page to non disambig. page 
                        if "album" and albumDetails["artists"][0]["name"].lower() in link.lower():
                            print(link.lower())
                            print("HIT ALBUM")
                            albumPage = wikiInit.page(link)
                            print("HIT LINK")
                            found_link = True                           # Set flag and break
                            break
                if found_link:
                    break
            displayPage = albumPage.summary                             # Wikipedia Page Changed here
        else:
            displayPage = "No Album Information found"


        # Begin Sending info Here
        await interaction.followup.send("Information Found!")
        await logChannel.send(f'1. Album Name: {albumDetails["name"]}')
        await logChannel.send(f'2. Album Type: {albumDetails["album_type"]}')

        # If multiple artists, send multiple
        if len(albumDetails["artists"]) > 1:
            await logChannel.send(f'3. Album Artists:')
            for artists in albumDetails["artists"]:
                await logChannel.send(f'\t{artists["name"]}')
        else:
            await logChannel.send(f'3. Album Artist: {albumDetails["artists"][0]["name"]}')
        
        # If multiple Genres, Send multiple
        if len(albumDetails["genres"]) > 1:
            await logChannel.send(f'4. Album Genres:')
            for genres in albumDetails["genres"]:
                await logChannel.send(f'\t{genres}')
        elif len(albumDetails["genres"]) == 1:
            await logChannel.send(f'4. Album Genre: {albumDetails["genres"]}')
        else:
            await logChannel.send(f'4. No Album Genre found')

        # Send rest of info
        await logChannel.send(f'5. Release Date: {albumDetails["release_date"]}')
        await logChannel.send(f'6. Number of Tracks: {albumDetails["total_tracks"]}')
        await logChannel.send(f'7. Album Label: {albumDetails["label"]}')
        await logChannel.send(f'8. Album Popularity: {albumDetails["popularity"]}')

        if len(displayPage) < 2000:                                     # Due to discord limitations, need to print description 2000 at a time
            await logChannel.send(f'9. Description: {displayPage}')     # If less than 2000, send immediately
        else:
            await logChannel.send(f'9. Description: ')
            newdisplay = ''                                             # Else, declare new variable to track 2000 chars at a time
            while len(displayPage) > 2000:                              # Iterate 2000 at a time 
                    
                newdisplay = displayPage[:2000]                         # string slicing to grab 2000 and send
                await logChannel.send(newdisplay)
                displayPage = displayPage[2000:]                        # YT description updated here          
            
            
            await logChannel.send(displayPage)                          # Send remainder of description




async def aboutTheArtist(interaction: discord.Interaction, client: discord.Client):
                                                                        # Song object Needs to exist before continuing
    await interaction.response.defer()
    if currentSongObj is None:                              
        await interaction.followup.send("Can't gather information from current song. No song is playing!")

    else:
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        initTitle = currentSongObj.title
        Title2 = initTitle.split(" - ")[0]                              # Split on - Separator (vast majority of youtube Videos)
        
                                                                        # Split on Quotes 
        if '"' in Title2:                                               
            Title2 = Title2.replace('"', '')

                                                                        # Search Spotify Artist field for New title
        titleToSearch = Title2
        searchResults = spotifyObj.search(q=titleToSearch, type="artist")

                                                                        # Case for no artist , Stop program execution
        if searchResults == {}:
            await interaction.followup.send("Error with Spotify Link Search: No Artists could be found")
            return

                                                                        # Acquire first Artist name from spotify Search
        artistSearch = searchResults["artists"]["items"][0]["external_urls"]["spotify"]
        artistDetails = spotifyObj.artist(artistSearch)                 # Return Artist object given name from spotify

                                                                        # Artist search failed here , stop program execution
        if "error" in artistDetails:                                    
            await interaction.followup.send("Error with Spotify Artist Search: Artist ID nonexistent")
            return

                                                                        # Acquire Artist name from Artist details field
        artistName = artistDetails["name"]
        print(artistDetails)                                            # Debug

        wikiInit = wikipediaapi.Wikipedia('en')                         # Search Wiki in English language for Artist Description
        artistPage = wikiInit.page(artistName)                          # Get first page given artist name 

        displayPage = artistPage.summary                                # Get wikipedia Summary From page
        
        # Begin Sends here
        await interaction.followup.send("Information Found!")
        await logChannel.send(f'1. Artist Name: {artistDetails["name"]}')
        await logChannel.send(f'2. Artist Popularity: {artistDetails["popularity"]}')
        await logChannel.send(f'3. Artist Followers: {artistDetails["followers"]["total"]}')

        if len(displayPage) < 2000:                                            # Due to discord limitations, need to print description 2000 at a time
            await logChannel.send(f'4. Artist Description: {displayPage}')     # If less than 2000, send immediately
        else:
            await logChannel.send(f'4. Artist Description: ')
            newdisplay = ''                                                    # Else, declare new variable to track 2000 chars at a time
            while len(displayPage) > 2000:                                     # Iterate 2000 at a time 
                    
                newdisplay = displayPage[:2000]                                # string slicing to grab 2000 and send
                await logChannel.send(newdisplay)
                displayPage = displayPage[2000:]                               # Wiki Description Updated here          
            
            
            await logChannel.send(displayPage)                                 # Send remainder of description

# Music Help Command function, displays all relevant functions for the music portion of the bot
async def musichelp(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send("**Music Help Master Sheet**\n")
    await interaction.followup.send(musicString)

# Adds a song to the front of the queue
async def addNext(interaction: discord.Interaction, client: discord.Client, url:str):
    await interaction.response.defer()
    global currentSongObj
    if currentSongObj != None and currentSongUrl!= '':
        print("Beginning of addNext")
        if (url.startswith('https://open.spotify.com/')) :                               # Check if Spotify Link
                    track_id = url.split('/')[-1]                                                # Strip '/' and strings after '?'
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
            
        songList.appendleft(filename)                                                               # Append new YouTube obj to top of the list
        print("Playnext: Song Appended")
        await interaction.followup.send(f'{filename.title} queued to play next ')
    
    else:
        await interaction.followup.send(' No song is currently playing. No queue to add song to! ')



# ============================================================================================================