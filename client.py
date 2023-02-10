# shbang
# Started 1/18/2023

import os
import discord
from discord import app_commands
from dotenv import load_dotenv

# setting up the needed intents
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# tree which will hold all of the client commands
tree = app_commands.CommandTree(client)

# the guildid of the server we want the bot to work in
guildId = 1063209733764435998

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=guildId))
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$bye'):
        await message.channel.send('Bye!')
    
    # await client.process_commands(message)

# Standard Slash Command Format
# sayhello command: Takes string input and bot will respond with hello to said string input
@tree.command(name = 'sayhello', description = 'Bot will respond with hello to the input given', guild=discord.Object(id=guildId))
@app_commands.describe(input="input")
async def say_hello(interaction: discord.Interaction, input: str):
    await interaction.response.send_message(f'Hello {input}!')
    
client.run(TOKEN)
