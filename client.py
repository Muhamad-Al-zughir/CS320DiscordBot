# shbang
# Started 1/18/2023

import os

import discord
from dotenv import load_dotenv

# setting up the needed intents
intents = discord.Intents.default()
intents.message_content = True  # setting message_content to True in order to read messages

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
