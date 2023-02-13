from discord.ui import Button
from discord.ui import View
from discord.ui import Select
import discord

#       ***************************************************************************************************
#       Notes:
#       data of all charcter will changeed to json in the future for now global for array list of characters
#       ****************************************************************************************************

#   ============
#   Player class
class Player:
    def __init__(self, nameUser,discord_identifation):
        self.name = nameUser
        self.userID = discord_identifation
        self.pg =0
        self.hitpoints = 1 
        self.strength = 0 
        self.defense = 0  
        self.inventory = []
        
    def showSelf(self):
        return (self.name + "\n" 
                "User ID key " + str(self.userID) + "\n"
                "hp: " + str(self.hitpoints) + "\n" 
                "strength: " + str(self.strength) + "\n" 
                "defense: " + str(self.defense) + "\n" 
                "Inventory Size: " + str(len(self.inventory))
        )
        
    def showInventory(self):
        if len(self.inventory) == 0:
            print("Nothing to show")
        else:
            for i in range(0, len(self.inventory)):
                print(self.inventory[i].showItem())
                print(self.inventory[i].showItemAttributes())
                
    def getPg(self):
        return self.pg
    
    def buy(self, cost):
        self.pg = self.pg - cost
    
    def gainPg(self, gain):
        self.pg = self.pg + gain
                
    def addItem(self, item):
        self.inventory.append(item)
        
    def boostAttack(self):
        self.strength = self.strength + 1
    
    def boostDefense(self):
        self.defense = self.defense + 1
    
    def boostHP(self):
        self.hitpoints = self.hitpoints + 1
#   =======================================

#   ==========
#   Item class
class Item:
    def __init__(self, itemName, strength, defense):
        self.name = itemName
        self.strength = strength 
        self.defense = defense
        self.pg = 0
        
    def showItem(self):
        return self.name
    def showItemAttributes(self):
        return "Strength: " + str(self.strength) + "\nDefense: " + str(self.defense) 
#   ================================================================================

#   ====================
#   AllPlayersData Class
#   ===================
class AllPlayersData():
    def __init__(self):
        self.playerList = []# players will be added to this list

#   return for player
    def returnPlayer(self, discord_identification):
        if len(self.playerList) == 0:
            return 0
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].userID == discord_identification):
                return self.playerList[i]
        return 0
            
#   search for player
    def searchforPlayer(self, discord_identification):
        if len(self.playerList) == 0:
            return 0
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].userID == discord_identification):
                return 1
        return 0
            
#   add player to list
    def addplayertoList(self, player):
        self.playerList.append(player)
#   ==================================

# Serverdata creation
serverPlayers = AllPlayersData()

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

#   ================
#   Class ItemButton
class ItemButton(Button):

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
#   should create a function witch sifts throuhg items such as stick and card and outputs corresponding embed
        if self.label == "stick":
#           create embed
            embed=discord.Embed(title="stick")
#           add parts
            embed.set_image(url="https://newsbugmedia.com/images/2022/05/stick-gun-shaped.jpg")

            
        elif self.label == "card":
        #   create embed
            embed=discord.Embed(title="Paul_Allens_card")
        #   add parts
            embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
    
        else:
        #   create embed
            embed=discord.Embed(title="broken_command_callback_itembutton")
        #   add parts
            embed.set_image(url="https://i0.wp.com/isaratech.com/wp-content/uploads/2018/03/2018-03-04.png")
        
    #   send to discord embed 
        await interaction.response.send_message(embed=embed)
#   ========================================================
 
#  =====================
#  show create character 
async def rp_character_create(interaction: discord.Integration):
    
    userID = interaction.user.id
    name = interaction.user.name
    
#       ****************
#       Notes:
#       data of all charcter will changeed to json in the future
#       ********************************************************

    if(serverPlayers.searchforPlayer(userID) != 0):
        await interaction.response.send_message("character already created for " + name)
        return

#   player creation
    player = Player(name, userID)
    
#   item creation
    stickItem = Item("stick", 1, 0)
    player.addItem(stickItem)
    stickItem = Item("card", 0, 0)
    player.addItem(stickItem)
        
    serverPlayers.addplayertoList(player)

    await interaction.response.send_message("character created for " + player.showSelf())
 
 #  =========
 #  show menu 
async def rp_dropdown_menu(interaction: discord.Interaction):
    
    name = interaction.user.name# to get user name have to do discord:interaction
    userID = interaction.user.id
    
    rp_character = serverPlayers.returnPlayer(userID)
    
#   if char doesnt exist exit
    if(rp_character == 0):
        await interaction.response.send_message("character not made yet for " + name)
        return
    
#   create embed
    embed=discord.Embed(title=str(rp_character.name), description="rp menu options" )
    embed.set_image(url="https://media.istockphoto.com/id/1130923888/vector/hand-with-dancing-puppet-vintage-background.jpg?s=612x612&w=0&k=20&c=nmYR7S7bgg1_22sqriEtcJAL-EuEfOeNXzJ4Zdgv2Mg=")

#   create Select dowpdown menu and and add it to view 
    select = DropdownMenu()
    view = View()
    view.add_item(select)
    
    await interaction.response.send_message(embed=embed, view=view)# send back embed as well as view
#   ================================================================================================ 
 
 #  ===========
 #  show player
async def rp_show_self(interaction: discord.Interaction):
    
    rp_character = serverPlayers.returnPlayer(interaction.user.id)
    
#   if char doesnt exist exit
    if(rp_character == 0):
        await interaction.response.send_message("character not made yet for " + interaction.user.name)
        return

#   inputs from character
    name_rp = rp_character.name
    statsHP = rp_character.hitpoints
    statsAtk = rp_character.strength
    statsDef = rp_character.defense
    statsGold = rp_character.pg
    
#   create embed
    embed=discord.Embed(title="Stats for " + name_rp)
        
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
    
#   amount of items user has for max size is 5 and gets it from user character "player"
    name = interaction.user.name# to get user name have to do discord:interaction
    userID = interaction.user.id
    
    rp_character = serverPlayers.returnPlayer(userID)
    inventorySize = len(rp_character.inventory)


#   create embed
    embed=discord.Embed(title="Inventory")
#   add parts
    embed.set_image(url="https://cdn11.bigcommerce.com/s-uiywfsyvbe/images/stencil/1280x1280/products/376/4053/4053__70532.1667672539.jpg?c=1")
    
#   create view
    view = View()
    
#   output all invbentory items make it into a function
    for i in range(0, inventorySize): # denots row in 
#       name of the item 
        button = ItemButton(rp_character.inventory[i].name, i)
        view.add_item(button)
        
    await interaction.response.send_message(embed=embed, view=view)# send back embed as well as view
 #  ======================================================================================


#   ============
#   store option
def storeDropdown(storeName):
    name = storeName
    
    print("Welcome to the store")
    print("my name is " + name)
    
#   display options fix later to show into disc with ui
    print("choose what you would like")
    print("attack boost")
    print("defense boost")
    print("hp boost")
    print("stick")
    print("Quit\n")
    
    return input()
#   ==============

#   =====
#   store
#   ========
def store(player):
    name = "Michaels"
    totalSpecialItems = 3
    
#   returns item selected from discord ui
    itemSelected = storeDropdown(name)

#   process
    print("choose what you would like")
    if itemSelected == "atk":
        if(player.getPg() >= 10):
            print("permanent raise to attack")
        else:
            print("failed to purchase")
    
    elif itemSelected == "def":
        if(player.getPg() >= 10):
            print("permanent raise to defense")
        else:
            print("failed to purchase")
    
    elif itemSelected == "hp":
        if(player.getPg() >= 10):
            print("permanent raise to hp")
        else:
            print("failed to purchase")
    
    elif itemSelected == "stick":
        if(player.getPg() >= 10):
            print("hello stick buyer")
        else:
            print("failed to purchase")
#   ===================================

#   for everymessage increase gold
def msgGold(player):
#   look for character adn chage it within char
    player.gainPg(10)

# testing and creationo of chracter, store, data list, item
# # player creation
# player = Player("bob")
# print(player.showSelf())
# player.showInventory()

# # item creation
# stickItem = Item("stick", 1, 0)
# player.addItem(stickItem)
# player.showInventory()

# # Serverdata creation
# serverPlayers = AllPlayersData()
# if(serverPlayers.searchforPlayer("bob") == 0):
#     print("not found player ")
    
# serverPlayers.addplayertoList(player)

# if(serverPlayers.searchforPlayer("bob") == 1):
#     print("found player")
    
# # store function
# store()
# print("\nmade it to end\n")
