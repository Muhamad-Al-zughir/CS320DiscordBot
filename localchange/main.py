
import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')
    Play = bot.get_cog('Play')
    await Play.check_skip.start()

bot.run(TOKEN)