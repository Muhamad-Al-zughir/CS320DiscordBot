# shbang
# Started 1/18/2023

import os

import discord
from dotenv import load_dotenv

# setting up the needed intents
intents = discord.Intents.all()
intents.message_content = True  # setting message_content to True in order to read messages

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# Code to respond to messages sent by users
@client.event
async def on_message(message):
    print(message)
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('/chiefkeef'):
        await message.channel.send("Fuckers in school telling me, always in the barber shop Chief Keef ain’t bout this, Chief Keef ain’t bout that My boy a BD on fucking Lamron and them He, he they say that nathan don’t be putting in no work SHUT THE FUCK UP! Y'all nathans ain’t know shit All ya motherfuckers talk about Chief Keef ain’t no hitta Chief Keef ain’t this Chief Keef a fake SHUT THE FUCK UP Y'all don’t live with that nathan Y'all know that nathan got caught with a ratchet Shootin' at the police and shit Nathan been on probation since fuckin, I don’t know when! Motherfuckers stop fuckin' playin' him like that Them nathans savages out there If I catch another motherfucker talking sweet about Chief Keef I’m fucking beating they ass! I’m not fucking playing no more You know those nathans role with Lil' Reese and them.")


client.run(TOKEN)
