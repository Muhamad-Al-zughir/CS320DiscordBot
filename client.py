# shbang
# Started 1/18/2023

import os

import discord
from discord import app_commands
from dotenv import load_dotenv
# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib as libby
import basic.methods as bm # basic methods contains functions that we will use a lot.

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

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Implement all the slash commands here, write down whos is which.
@tree.command(name = "libgen", description = "Search for books")
@app_commands.describe(type="Please enter either \"author\" or \"title\"", search="Search, must be at least 3 characters")
async def basic_libgen(interaction, type: str, search: str): # Set the arguments here to get options on the slash commands.
    res = libby.handleValidation(type, search)
    if (res != True):
        await bm.send_msg(interaction, res)
    else:
        results = libby.basicSearch(type, search)
        strings = libby.formatResults(results)
        msg = '\n'.join(strings)
        await bm.send_msg(interaction, msg)
    reply = await client.wait_for('message')
    try:
        num = int(reply.content)
        if (num > len(strings) or num < 1): raise ValueError("outside bounds")
    except ValueError:
        await bm.follow_up(interaction, "Not a number between 1-" + str(len(strings))) # Need to use a follow up after initial sending
        return
    obj = results[num]
    links = libby.getLinksFor(obj)
    strings2 = libby.formatLinks(links)
    msg = '\n'.join(strings2)
    await bm.follow_up(interaction, msg)

# Add new slash commands beneath this


@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    if message.author == client.user:
        return
        
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('/chiefkeef'):
        await message.channel.send("Fuckers in school telling me, always in the barber shop Chief Keef ain’t bout this, Chief Keef ain’t bout that My boy a BD on fucking Lamron and them He, he they say that nathan don’t be putting in no work SHUT THE FUCK UP! Y'all nathans ain’t know shit All ya motherfuckers talk about Chief Keef ain’t no hitta Chief Keef ain’t this Chief Keef a fake SHUT THE FUCK UP Y'all don’t live with that nathan Y'all know that nathan got caught with a ratchet Shootin' at the police and shit Nathan been on probation since fuckin, I don’t know when! Motherfuckers stop fuckin' playin' him like that Them nathans savages out there If I catch another motherfucker talking sweet about Chief Keef I’m fucking beating they ass! I’m not fucking playing no more You know those nathans role with Lil' Reese and them.")

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
