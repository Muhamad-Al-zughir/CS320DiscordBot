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



# setting up the needed intents
intents = discord.Intents.all()
intents.message_content = True  # setting message_content to True in order to read messages
client = discord.Client(intents=intents)

# tree which will hold all of the client commands
tree = app_commands.CommandTree(client)

# the guildid of the server we want the bot to work in
guildId = 1063209733764435998

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

# Member list of people in channel to be streamed to
streaming_members = {}

# YouTube options list set to best audio settings
# Setting options found from youtube-dl documentation
# https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
yt_params = {'format' :  'bestaudio/best'}
yt_streamObj = youtube_dl.YoutubeDL(yt_params)

# ffmpeg params set to disable video
# Settings found from https://ffmpeg.org/ffmpeg.html
ff_params = {'options' : '-vn'}

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildId))
    print(f'{client.user} has connected to Discord!')


# Standard Slash Command Format
# sayhello command: Takes string input and bot will respond with hello to said string input
@tree.command(name = 'sayhello', description = 'Bot will respond with hello to the input given', guild=discord.Object(id=guildId))
@app_commands.describe(input="input")
async def say_hello(interaction: discord.Interaction, input: str):
    await interaction.response.send_message(f'Hello {input}!')


@tree.command(name = 'join', description = 'Bot will join your voice channel', guild=discord.Object(id=guildId))
#@app_commands.describe(input="input")
async def join(interaction: discord.Interaction, channel: discord.VoiceChannel):
        """Joins a voice channel"""
        try:
            await interaction.response.send_message(f'Joining {channel}')
            voice = interaction.guild
            if voice.voice_client is not None:
                return await voice.voice_client.move_to(channel)

            await channel.connect()

        except Exception as err:
            print(err)

client.run(TOKEN)
