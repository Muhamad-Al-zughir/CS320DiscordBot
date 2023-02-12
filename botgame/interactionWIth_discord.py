import os

import discord
from discord import app_commands
from discord.ui import Button
from discord.ui import View
from dotenv import load_dotenv
# all this is has is very basic interactions with discord /
#  commands and buttons along with select along
#   everything above and at the very end is the same as the start and end of client.py


# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
#   ===================================


# second test
@tree.command(name = "weare", description = "2nd command")
async def anotherone(interaction, input: str):
    await interaction.response.send_message("I dont know about you but me personaly dont like: " + input)
    
# third test
@tree.command(name = "tragic_abs", description = "my third comm")
async def embeddy(interactions: discord.Interaction):
    name = interactions.user.name# to get user name have to do discord:Interactions
    embed=discord.Embed(title=str(name), 
                        description="So long and good night\n          - Helena", 
                        color=0x00ff4c
                        )
    embed.add_field(name="John cena", value="invisMan")
    embed.set_image(url="https://yt3.googleusercontent.com/5_zhwJpxRMYg3QjRcQbta3ewQUbV3mEAbiUqMD-N5CWUDM8znqhhxcDlFKoAc_v5fljg3cZYqg=s900-c-k-c0x00ffffff-no-rj")
    embed.set_thumbnail(url="https://yt3.googleusercontent.com/5_zhwJpxRMYg3QjRcQbta3ewQUbV3mEAbiUqMD-N5CWUDM8znqhhxcDlFKoAc_v5fljg3cZYqg=s900-c-k-c0x00ffffff-no-rj")
    await interactions.response.send_message(embed=embed)

# first test
@tree.command(name = "firstwrd", description = "first command")
async def talkintalkintalk(interaction):
    await interaction.response.send_message("hellowrld")

# 4th test
@tree.command(name = "summonbutonus", description = "4th app command")
async def botunus(interaction):
    button = Button(label="KIllme", 
                    style=discord.ButtonStyle.green
                )# can be set to different styles and colors
    view = View()
    view.add_item(button)
    
    async def buttonscallback(interaction):
        await interaction.response.edit_message(content="iya!", view=None)
        await interaction.followup.send("Success") 
    button.callback = buttonscallback
       
    await interaction.response.send_message("Hello!", view=view)
    
# fifth test    
@tree.command(name = "summon_inv", description = "5th Command")
async def dadsShoppinglist(interaction):
    
    select = discord.ui.Select(  
        placeholder = "DadsShoppingList",
        min_values = 1, #min and max select times
        max_values = 1,
        options = [ # emoji does not work dont knwo why
            discord.SelectOption(
                label="Snow",
                description="Just remember it doesn't warm you in December"
            ),
            discord.SelectOption(
                label="Clouds",
                description="Pain",
            ),
            discord.SelectOption(
                label="Cigarettes",
                description="marls are the best much better than the 4 legged desert deer"
            ),
            discord.SelectOption(
                label="milk",
                description="a rare item"
            )
        ]
    )
    
    view = View()
    view.add_item(select)
    
    async def buttonscallback(interaction):
        await interaction.response.edit_message(content="iya!", view=None)
        await interaction.followup.send("Success") 
    select.callback = buttonscallback
    
    await interaction.response.send_message("Inventory List", view=view)

#   ========================
#   so end of client.py copy
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
client.run(TOKEN)
