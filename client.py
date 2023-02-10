# shbang
# Started 1/18/2023

import os
import discord
from dotenv import load_dotenv

# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('!bye'):
        await message.channel.send('Bye!')
        
client.run(TOKEN)
