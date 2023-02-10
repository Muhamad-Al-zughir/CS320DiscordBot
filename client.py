# shbang
# Started 1/18/2023

import os

import discord
from discord import app_commands
from dotenv import load_dotenv

# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')
TEST_TOKEN = os.getenv('TEST_CHANNEL')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Implement all the slash commands here
@tree.command(name = "libgen", description = "Trying things out", options=)
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
