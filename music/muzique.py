# # shbang
# # Started 1/18/2023

# # Imports
# import os
# import asyncio
# import discord
# from discord.ext import commands
# from discord import app_commands
# from dotenv import load_dotenv
# import youtube_dl
# import ffmpeg


# # setting up the needed intents
# intents = discord.Intents.all()
# intents.message_content = True  # setting message_content to True in order to read messages
# client = discord.Client(intents=intents)

# # tree which will hold all of the client commands
# tree = app_commands.CommandTree(client)

# load_dotenv() # loads all the content in the .env folder
# TOKEN = os.getenv('DISCORD_API')

# # Member list of people in channel to be streamed to (used later)
# streaming_members = {}

# # YouTube options list set to best audio settings
# # Setting options found from youtube-dl documentation
# # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
# yt_params = {'format' :  'bestaudio/best'}
# yt_streamObj = youtube_dl.YoutubeDL(yt_params)

# # ffmpeg params set to disable video
# # Settings found from https://ffmpeg.org/ffmpeg.html
# ff_params = {'options': '-vn'}


# # ** NOTE **
# # Class YouTube_linkobj below is borrowed from https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py 

# class YouTube_linkobj(discord.PCMVolumeTransformer):
#     def __init__(self, source, *, data):
#         super().__init__(source)
       
#         self.data = data
#         self.title = data.get('title')
#         self.url = data.get('url')

#     @classmethod
#     async def from_url(cls, url, *, loop=None, stream=False):
#         loop = loop or asyncio.get_event_loop()
#         data = await loop.run_in_executor(None, lambda: yt_streamObj.extract_info(url, download=not stream))

#         if 'entries' in data:
#             data = data['entries'][0]       # 1st item in playlist index

#         filename = data['url'] if stream else yt_streamObj.prepare_filename(data)
#         return cls(discord.FFmpegPCMAudio(filename, **ff_params), data=data)       # Return discord.ffmpegpcm audio class 

# @client.event
# async def on_ready():
#     await tree.sync()
#     print(f'{client.user} has connected to Discord!')


# @tree.command(name = 'move', description = 'Bot will join your voice channel')
# async def move(interaction: discord.Interaction):     
#         try:
#             await interaction.response.send_message(f'Joining...')                  # Sends attempt message to server
#             local = interaction.guild                                               # Create local instances of guild and check for existence of voice client
#             voicechan = local.voice_client      
#             if voicechan is not None:                                               # Voice channel exists, move to caller's channel
#                 return await voicechan.move_to(interaction.user.voice.channel)

#             await interaction.user.voice.channel.connect()                          # Establish connection after move



#         except Exception as err:                                                    # Display general catch-all error for debug purposes
#             print(err)

# # Streams from a YouTube Link
# @tree.command(name = 'play_yt', description = 'Bot will play from a valid YouTube Link')
# async def play_youtube(interaction: discord.Interaction, url:str):

#         print("Join being attempted ..")
#         local = interaction.guild                                                  # Establish server context
#         voicechan = local.voice_client                                             # Establish related voice channel
        
#         if voicechan is not None:                                                  # Disconnect if the bot is already in a voicechannel
#             print("Bot currently not in channel\nJoining...")
#             await local.voice_client.disconnect()
        
#         await interaction.user.voice.channel.connect()

#         server = interaction.guild                                                 # Re-establish server context and voice client after connection
#         voice_channel = server.voice_client                                       
        
#         print("Before retrieving YouTube Object...")
#         filename = await YouTube_linkobj.from_url(url, loop=client.loop, stream=True)

#         print("Before Playing in channel...")
#         voice_channel.play(filename)

#         print("Before user-end interaction message...")
#         await interaction.response.send_message(f'Now playing {filename.title}') 
               
#         print("Reached here in command")                                           # Debug statements

# # End Stream
# @tree.command(name = 'clear', description = 'Bot will clear all playing music')
# async def clear(interaction: discord.Interaction):
#     server = interaction.guild
#     voice_channel = server.voice_client

#     await voice_channel.disconnect()
#     await interaction.response.send_message(f'Music has been stopped')


# # Pause Stream and Unpause Stream
# @tree.command(name = 'pause-unpause', description = 'Bot will pause the currently playing song or unpause if one was being played')
# async def pause_yt(interaction: discord.Interaction):
    
#     vcstatus = interaction.guild.voice_client
#     if vcstatus.is_playing():
#         vcstatus.pause()
#         await interaction.response.send_message('player is now paused')
#     elif vcstatus.is_paused():
#         vcstatus.resume()
#         await interaction.response.send_message('player is now un-paused')
#     else:
#         await interaction.response.send_message('Nothing is currently playing')

