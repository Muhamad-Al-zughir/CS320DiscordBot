# shbang
# Started 1/18/2023

import os

import discord
from discord import app_commands
from dotenv import load_dotenv
# Add your imports below here, if in a folder, use a dot instead of a slash
import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.

# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Implement all the slash commands here, write down whos is which.
@tree.command(name = "libgen", description = "Search for books")
async def basic_libgen(interaction, type: str, search: str): # Set the arguments here to get options on the slash commands.
    res = libby.handleValidation(type, search)
    if (res != True):
        await bm.send_msg(interaction, res)
    else:
        results = libby.basicSearch(type, search)
        strings = libby.formatResults(results)
        msg = '\n'.join(strings)
        await bm.send_msg(interaction, msg)

# sayhello command: Takes string input and bot will respond with hello to said string input
@tree.command(name = 'sayhello', description = 'Bot will respond with hello to the input given')
async def say_hello(interaction: discord.Interaction, input: str, name: str):
    await interaction.response.send_message(f'Hello {input}! name={name}')

# spidergif command: After the running of the command the bot will respond by posting a funny spider gif
@tree.command(name = 'spidergif', description = 'Bot will post a funny spider gif')
async def say_hello(interaction: discord.Interaction):
    await interaction.response.send_message('https://tenor.com/view/to-everyone-that-is-looking-for-this-spider-gif-gif-20691150')

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

# Code to respond to any messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$bye'):
        await message.channel.send('Bye!')

client.run(TOKEN)
