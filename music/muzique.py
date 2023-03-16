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

# Song List for Queuing
songList = deque()
currentSongUrl = ''
currentSongObj = None


# ** NOTE **
# Class YouTube_linkobj below is borrowed from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py 
# FFMPEG options for seeking found from https://stackoverflow.com/questions/7945747/how-can-you-only-extract-30-seconds-of-audio-using-ffmpeg
class YouTube_linkobj(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data):
        super().__init__(source)
       
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')
        self.songTime = data.get('duration')
        self.startTime = 0


    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False, start=0):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: yt_streamObj.extract_info(url, download=not stream))

        newTime = start
        ff_params = {'options': f'-vn -ss {newTime}',
             'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
        

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
        ff_params = {'options': f'-vn -ss {newTime}',
             'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

        
        print(f'newtime is {newTime}')
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['url'] if stream else yt_streamObj.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ff_params), data=data)


# ================================================================================== Universal / Sys functions

# End Stream | Universal
async def clear(interaction: discord.Interaction):
    server = interaction.guild
    voice_channel = server.voice_client

    if voice_channel is None:
        await interaction.response.send_message(f'There is no music to clear!')
    else:
        await voice_channel.disconnect()
        songList.clear()
        await interaction.response.send_message(f'Music has been stopped & the queue has been cleared')

# Pause Stream and Unpause Stream | Universal
async def pause_yt(interaction: discord.Interaction):
    
    vcstatus = interaction.guild.voice_client
    if vcstatus is None:
        await interaction.response.send_message('Nothing is currently playing')
    elif vcstatus.is_playing():
        vcstatus.pause()
        await interaction.response.send_message('player is now paused')
    elif vcstatus.is_paused():
        vcstatus.resume()
        await interaction.response.send_message('player is now un-paused')
    else:
        await interaction.response.send_message(f'Unknown error in PAUSE occured')

# Move / Join command | Universal
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

# ============================================================================================================
#
# ================================================================================== Playback Centric Functions

# Play from a link | YouTube , SoundCloud, and Spotify!
async def play(interaction: discord.Interaction, url:str, client: discord.Client):
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
            await interaction.response.send_message(f'Added {filename.title} to queue')             # Send user friendly message

        else:                                                                                       # Else, begin playing the next song
            voice_channel.play(filename, after=lambda next: nextSong(interaction, client))          # Upon .play operation ending, after uses lambda function next
            print("Before user-end interaction message...")                                         # Calls upon nextSong given interaction and client to loop through queue
            currentSongUrl = filename.title
            currentSongObj = filename
            await interaction.response.send_message(f'Now playing {filename.title}')                # Happens for every song until queue is empty

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
        #                 https://stackoverflow.com/questions/65768920/how-to-make-a-discord-music-bot-to-recognize-the-end-of-song-or-where-it-is-play
        #                 https://docs.python.org/3/library/asyncio-task.html#scheduling-from-other-threads

    else:                                                                                           # No songs in queue, disconnect
        asyncio.run_coroutine_threadsafe(interaction.guild.voice_client.disconnect(), client.loop)
        currentSongUrl=''
        currentSongObj = None

    print("NEXT SONG COMPLETE")

# Skipping songs function
async def skipSong(interaction: discord.Interaction, client: discord.Client):
    #print("Before Skip")                                                                       # Debug Prints
    print(songList)
    local = interaction.guild                                                                   # Establish server context
    voicechan = local.voice_client                                                              # Establish related voice channel

    if voicechan is None:
        await interaction.response.send_message(f'No current song playing to skip!')
    elif voicechan.is_playing():
        await interaction.response.send_message(f'Skipping song')
        voicechan.stop()
    else:
        await interaction.response.send_message(f'Unknown error in SKIP occured')
    #print("After Skip") 
    #print(songList)

# Displays the current queue of songs to be played
async def displayQueue(interaction: discord.Interaction, client: discord.Client):
    if len(songList) != 0:                                                           
        await interaction.response.send_message(f'Current Queue is:')
        logId = interaction.channel_id
        logChannel = client.get_channel(logId)
        i = 1
        for songs in songList:
            display = songs.title
            display = str(i) + ": " + display
            await logChannel.send(display)
            i = i+1
    else: 
        await interaction.response.send_message(f'No active Queue to be displayed!')

# Shuffles the Current Queue of Songs and Redisplays it
async def shuffleQueue(interaction: discord.Interaction, client: discord.Client):
    if len(songList) != 0:
        await interaction.response.send_message(f'Queue Shuffled. Current Queue is now:')

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
        await interaction.response.send_message(f'No active Queue to be shuffled!')


# Shifting The Track
async def fastForwardSong(interaction: discord.Interaction, client: discord.Client, seconds: int):
    local = interaction.guild                                                                   # Establish server context
    voicechan = local.voice_client   
    #global currentSongTime
    print("CURRNET SONG LISTS ARE")
    print(songList)
    print("Reached Fast Forward")                                                          # Establish related voice channel
    if currentSongUrl !='':
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
            await interaction.response.send_message(f'Fast Forwarding..')
        
        else:
            await interaction.response.send_message(
                f'Invalid Number of Seconds Entered (check that the value is not 0, and the seconds does not exceed the duration of the song)') 





# ============================================================================================================

