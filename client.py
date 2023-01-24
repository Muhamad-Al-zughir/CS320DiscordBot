# shbang
# Started 1/18/2023

import os

import discord
from dotenv import load_dotenv

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
