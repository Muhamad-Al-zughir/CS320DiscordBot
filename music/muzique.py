# shbang
# Started 1/18/2023

# Imports
import os
import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import youtube_dl
import ffmpeg
import wavelink
from wavelink.ext import spotify


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

# Spotify Developer Tokens
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

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

"""
#  ** Start **
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
"""

# ================================================================================== Universal / Sys functions

# End Stream | Universal

async def clear(interaction: discord.Interaction):
    server = interaction.guild
    voice_channel = server.voice_client

    await voice_channel.disconnect()
    await interaction.response.send_message(f'Music has been stopped')

# Pause Stream and Unpause Stream | Universal

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
# ================================================================================== YouTube Centric Functions
# Play from a link | YouTube & SoundCloud

async def play_youtube(interaction: discord.Interaction, url:str, client: discord.Client):

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

# ============================================================================================================
#
# ============================================================================================= Spotify Client

     
async def create_nodes(interaction: discord.Interaction,client: discord.Client):
    await wavelink.NodePool.create_node(bot = client,
                                        host = "lavalink.sneakynodes.com",
                                        port = 2333,
                                        password = "sneakynodes.com",
                                        https = False,                  # might change
                                        spotify_client=spotify.SpotifyClient(client_id=spotify_client_id, client_secret=spotify_client_secret)
                                        )

async def play_spotify(interaction: discord.Interaction, url:str, client: discord.Client):
     await spotify.SpotifyTrack.search(query=url, return_first=True)