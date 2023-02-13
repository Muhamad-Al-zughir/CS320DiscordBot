import os

import discord
from discord import app_commands
from discord.ui import Button
from discord.ui import View
from discord.ui import Select
from dotenv import load_dotenv
# Add your imports below here, if in a folder, use a dot instead of a slash

# setting up the needed intents
intents = discord.Intents.all()

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
#   ****************************************************************************

#   ==================
#   Class Dropdownmenu
class DropdownMenu(Select):

#   ===========
#   constructor
    def __init__(self) -> None:
        super().__init__(
            placeholder = "Menu Options",
            min_values = 1, #min and max select times
            max_values = 1,
            options = [ # emoji does not work dont knwo why
                discord.SelectOption(
                    label="Show Character",
                    description="Shows all character stats as well as gold",
                ),
                discord.SelectOption(
                    label="Inventory",
                    description="shows inventory"
                ),
                discord.SelectOption(
                    label="Challenge",
                    description="you are not allowed to that yet"
                ),
            ]
        )
#       =
        
#   callback function
    async def callback(self, interaction: discord.Integration):

#       if Char
        if self.values == ['Show Character']:
            await rp_show_self(interaction)
            
#       if Char
        if self.values == ['Inventory']:
            await rp_inventory(interaction)
        
#       if Char
        if self.values == ['Challenge']:
            name = interaction.user.name# to get user name have to do discord:interaction
        
        #   create embed
            embed=discord.Embed(title="Challenge",  description="fighting thing")
            embed.set_image(url="https://e7.pngegg.com/pngimages/10/113/png-clipart-bob-hoskins-super-mario-bros-mario-luigi-superstar-saga-embroidered-tshirt-super-mario-bros-thumbnail.png")
            await interaction.response.send_message(embed=embed)# send back embed as well as view
#   =============================================================

#   ===================
#   Class DefaultButton
class DefaultButton(Button):

#   ===========
#   constructor
    def __init__(self, buttonName, ith):
        super().__init__(
            label=buttonName, 
            style=discord.ButtonStyle.gray,
            row=ith
        )
#       =
        
#   callback function
    async def callback(self, interaction):
        await interaction.response.send_message(self.label)
#   =========================================================

#   =====================================
#   dropdown menu for character selection
@tree.command(name = "rp_menu", description = "menu options for rp game")
async def rp_dropdown_menu(interaction: discord.Interaction):
    
    name = interaction.user.name# to get user name have to do discord:interaction
    
#   create embed
    embed=discord.Embed(title=str(name), description="rp menu options" )
    embed.set_image(url="https://media.istockphoto.com/id/1130923888/vector/hand-with-dancing-puppet-vintage-background.jpg?s=612x612&w=0&k=20&c=nmYR7S7bgg1_22sqriEtcJAL-EuEfOeNXzJ4Zdgv2Mg=")

#   create Select dowpdown menu and and add it to view 
    select = DropdownMenu()
    view = View()
    view.add_item(select)
    
    await interaction.response.send_message(embed=embed, view=view)# send back embed as well as view
 #  ================================================================
 
 #  ===========
 #  show player
async def rp_show_self(interaction: discord.Interaction):
    
    name = interaction.user.name# to get user name have to do discord:interaction
    
#   create embed
    embed=discord.Embed(title="Stats")
    
#   inputs from character
    statsHP = str(100)
    statsAtk = str(100)
    statsDef = str(100)
    statsGold = str(100)
    
#   add parts
    embed.add_field(name="HP", value=statsHP)
    embed.add_field(name="Attack", value=statsAtk)
    embed.add_field(name="Defense", value=statsDef)
    embed.add_field(name="Gold", value=statsGold)
    embed.set_image(url="https://res.cloudinary.com/teepublic/image/private/s--HHH2GMBP--/t_Resized%20Artwork/c_fit,g_north_west,h_954,w_954/co_000000,e_outline:48/co_000000,e_outline:inner_fill:48/co_ffffff,e_outline:48/co_ffffff,e_outline:inner_fill:48/co_bbbbbb,e_outline:3:1000/c_mpad,g_center,h_1260,w_1260/b_rgb:eeeeee/c_limit,f_auto,h_630,q_90,w_630/v1557411414/production/designs/4802849_0.jpg")
    await interaction.response.send_message(embed=embed)# send back embed as well as view
#   ================================================================
 
 #  ==============
 #  show inventory
async def rp_inventory(interaction: discord.Interaction):
    
#   amount of items user has for max size is 5
    rp_inventorySize = 5
    name = interaction.user.name# to get user name have to do discord:interaction
    
#   create embed
    embed=discord.Embed(title="Stats")
#   add parts
    embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
    
#   create view
    view = View()
    
#   output all invbentory items
    for i in range(rp_inventorySize):
#       name of the item 
        button = DefaultButton("stick", i)
        view.add_item(button)
        
    await interaction.response.send_message(embed=embed, view=view)# send back embed as well as view
 #  ======================================================================================

#   ****************************************************************************
#   end

@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
    
#   =============================    
#   will gift players gold on msg
#   had to make author == user check or else it would go for infinity 
@client.event
async def on_message(message):
    if message.author == client.user:
        return
#   else run function to add gold to player
#   rpMsgReward()

client.run(TOKEN)


