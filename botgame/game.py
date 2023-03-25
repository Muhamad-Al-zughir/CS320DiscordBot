from discord.ui import Button
from discord.ui import View
from discord.ui import Select
from discord.utils import get
from discord import Member
# from apscheduler.schedulers.blocking import AsyncIOScheduler
import discord
import random

# just seeds random
random.seed(2)

#       ***************************************************************************************************
#       Notes:
#       data of all charcter will changeed to json in the future for now global for array list of characters
#       other note needs to download pip install apscheduler to run schedled events
#       ****************************************************************************************************

#   ============
#   Player class
class Player:
    def __init__(self, nameUser,discord_identifation):
        self.name = nameUser
        self.userID = discord_identifation
        self.pg = 100
        self.hitpoints = 1 
        self.strength = 0 
        self.defense = 0  
        self.inventory = []
        self.equipped = []
        self.msgActivity =0# could be its own array
        self.inActive_warningS =0# could be its own array
        
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
                
    def searchPlayerInventory(self,itemName):
        if len(self.inventory) == 0:
            return 0
        else:
            found = 0 
            for i in range(0, len(self.inventory)):
                if(self.inventory[i].name == itemName):
                    found = 1
            return found

    def returnPlayerInventory(self,itemName):
        for i in range(0, len(self.inventory)):
            if(self.inventory[i].name == itemName):
                itemObj =  self.inventory[i]
        return itemObj
        
#   yeah fix it later sell but buy works idk m8                
    # def sellToStore(self):
    #     self.inventory[i].name = someFunction()
    #     self.sell(item)
    def getName(self):
        return self.name
    def getUserID(self):
        return self.userID

    def getStrength(self):
        return self.strength
    def getDefense(self):
        return self.defense
    def getPg(self):
        return self.pg
    
    def getInventorySize(self):
        return len(self.inventory)
    def getEquippedSize(self):
        return len(self.equipped)
    def getinActive_warningS(self):
        return self.inActive_warningS
    def getItem(self, location):
        return self.inventory[location]
    def getEquippedItem(self, location):
        return self.equipped[location]
    def getmsgAct(self):
        return self.msgActivity
    
    def getUserID(self):
        return self.userID
 
    def clearMsgHist(self):
        self.msgActivity = 0
    
    def addtoIA(self):#add to inactivty
        self.inActive_warningS = self.inActive_warningS + 1
    def buy(self, cost):
        self.pg = self.pg - cost
    def sell(self, item):
        self.pg = self.pg + item.pg
        self.inventory.remove(item)
    def gainPg(self, gain):
        
        self.pg = self.pg + gain
    def addItem(self, item):
        self.inventory.append(item)
    def equipItem(self, item):
        self.equipped.append(item)
    def boostAttack(self, boost):
        self.strength = self.strength + boost
    def boostDefense(self):
        self.defense = self.defense + 1
    def boostHP(self):
        self.hitpoints = self.hitpoints + 1
#   =======================================

#   =======================================
#   Player class use to clean up code later
class Store:

#   two inventories for the store
#   inventory: one for selling 
#   inventoryBuyBack: for letting player buy back item
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.inventoryBuyBack = []
        # could add features such as how many items sold 
        # maybe own rng for specialty items 
        
#   for debugging  
    def showSelf(self):
        return (self.name + "\n" +
                "StoreName " + str(self.name) + "\n" +
                "Inventory Size: " + str(len(self.inventory)) +
                "Inventory Size: " + str(len(self.inventoryBuyBack))
                )

    def showInventoryBuyBack(self):
        if len(self.inventory) == 0:
            print("Nothing to show")
        else:
            for i in range(0, len(self.inventory)):
                print(self.inventory[i].showItem())
                print(self.inventory[i].showItemAttributes())

    def getPg(self):
        return self.pg
    
    def getInventoryBuyBackSize(self):
        return len(self.inventoryBuyBack)
        
    def sell(self, item):
        self.inventoryBuyBack.remove(item)
    
    def addItem(self, item):
        self.inventoryBuyBack.append(item)
#   ======================================

#   ==========
#   Item class
class Item:
    def __init__(self, itemName, strength, defense, pg):
        self.name = itemName
        self.strength = strength 
        self.defense = defense
        self.pg = pg
        
    def showItem(self):
        return self.name
    def showItemAttributes(self):
        return "Strength: " + str(self.strength) + "\nDefense: " + str(self.defense) 
    def getStrengthItem(self):
        return self.strength
    def getDefenseItem(self):
        return self.defense
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
            
#   search for player return 1 if exists else 0 
    def searchforPlayer(self, discord_identification):
        if len(self.playerList) == 0:
            return 0
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].userID == discord_identification):
                return 1
        return 0
    
    def deletePlayer(self, discord_identification):
#       search for player return -1 not found 
        if len(self.playerList) == 0:
            return -1
#       doesnt exist else delete player and return 0 
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].userID == discord_identification):
                self.playerList.pop(i)
                return 0
        return -1

#   return player in spot loc
    def getPlayerat_loc(self,loc):
        return self.playerList[loc]        
            
#   add player to list
    def addplayertoList(self, player):
        self.playerList.append(player)

    def getAllPlayersDataSize(self):
        return len(self.playerList)
#   ===============================      

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
        #   create embed
            embed=discord.Embed(title="Paul_Allens_card")
        #   add parts
            embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
            
        elif self.label == "card":
        #   create embed
            embed=discord.Embed(title="Paul_Allens_card")
        #   add parts
            embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
    
        elif self.label == "angel wings":
        #   create embed
            embed=discord.Embed(title=self.label)
        #   add parts
            embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
    
        elif self.label == "steetware":
        #   create embed
            embed=discord.Embed(title=self.label)
        #   add parts
            embed.set_image(url="https://i.seadn.io/gae/LIoXlDW3hzLtQeB6tfOqVC8yvlCsXk6YCMNHu2ixJhl74-bldzJDxJXpCM6p9Vk6MF3g9eeDDZE0zTJvjD9wTYO0xAoQsmLFQvmLffs?auto=format&w=1000")
    
        elif self.label == "pickaxe":
        #   create embed
            embed=discord.Embed(title=self.label)
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

#   ======================
#   Class StoreItem_Button
class StoreItem_Button(Button):

#   ===========
#   constructor
    def __init__(self, buttonName):
        super().__init__(
            label=buttonName, 
            style=discord.ButtonStyle.gray
        )
#       =
        
#   callback function
    async def callback(self, interaction):
#   should create a function witch does this but for now will leave 
#   should also create a function of just the items default
#       get players userID that called interaction
        userID = interaction.user.id
    
#       player not found cant purchase from store 
        if serverPlayers.searchforPlayer(userID) == 0:
            await interaction.response.send_message("Character not made cannot purchase I am sorry" + interaction.user.name)
            return
        
#       GET PLAYER
        user_rp_char = serverPlayers.returnPlayer(userID)
    
#       check if enough space to purchase more
        if self.label == "sell" and (user_rp_char.getInventorySize()  >= 1):
            user_rp_char.sell()
            await interaction.response.send_message("you sold" + interaction.user.name)
    
#       check if enough space to purchase more
        if user_rp_char.getInventorySize() > 3:
            await interaction.response.send_message("you cant have anymore items sorry" + interaction.user.name)
            return

#       else check all item options as well as if user has enough gold 
        elif self.label == "stick" and (user_rp_char.getPg()  >= 1):
            item = Item("stick", 1, 0, 1)
            user_rp_char.buy(1)
            user_rp_char.addItem(item)
            response_to_Buyer = "You have successfully bought " + self.label
            
        elif self.label == "card" and (user_rp_char.getPg() >= 5):
            item = Item("card", 1, 2, 5)
            user_rp_char.buy(5)
            user_rp_char.addItem(item)
            response_to_Buyer = "You have successfully bought " + self.label
    
        elif self.label == "streetware" and (user_rp_char.getPg() >= 30):
            item = Item("streetware", 10, 30 , 30)
            user_rp_char.buy(30)
            user_rp_char.addItem(item)
            response_to_Buyer = "You have successfully bought " + self.label
               
        elif self.label == "pickaxe"  and (user_rp_char.getPg() >= 15):
            item = Item("pickaxe", 10,0 ,15)
            user_rp_char.buy(15)
            user_rp_char.addItem(item)
            response_to_Buyer = "You have successfully bought " + self.label
                
        elif self.label == "angel wings"  and (user_rp_char.getPg() >= 50):
            item = Item("angel wings", 25, 25, 50)
            user_rp_char.buy(50)
            user_rp_char.addItem(item)
            response_to_Buyer = "You have successfully bought " + self.label
            
        else:
            response_to_Buyer = "You are a broke and failed to buy a " + self.label
        
    #   send to discord embed 
        await interaction.response.send_message(response_to_Buyer + " " + interaction.user.name)
#   ============================================================================================

#   just to help organize
def storeItemsresponses(nameofThing, buyersWalletSize):
#       else check all item options as well as if user has enough gold 
    if nameofThing == "stick" and (buyersWalletSize  >= 1):
            response_to_Buyer = "You have successfully bought " + nameofThing
            
    elif nameofThing == "card" and (buyersWalletSize >= 5):
            response_to_Buyer = "You have successfully bought " + nameofThing
    
    elif nameofThing == "streetware" and (buyersWalletSize >= 30):
            response_to_Buyer = "You have successfully bought " + nameofThing
               
    elif nameofThing == "pickaxe"  and (buyersWalletSize>= 15):
            response_to_Buyer = "You have successfully bought " + nameofThing
                
    elif nameofThing == "angel wings"  and (buyersWalletSize >= 50):
            response_to_Buyer = "You have successfully bought " + nameofThing
            
    else:
        response_to_Buyer = "You are a broke and failed to buy a " + nameofThing
            
    return response_to_Buyer

def storeItemsInteractionWithBuyer(player, nameofThing):
#   do stuff to buyer 
    if nameofThing == "stick" and (player.getPg()  >= 1):
        item = Item("stick", 1, 0, 1)
        player.buy(1)
        player.addItem(item)
            
    elif nameofThing == "card" and (player.getPg() >= 5):
        item = Item("card", 1, 2, 5)
        player.buy(5)
        player.addItem(item)
    
    elif nameofThing== "streetware" and (player.getPg() >= 30):
        item = Item("streetware", 10, 30 , 30)
        player.buy(30)
        player.addItem(item)
               
    elif nameofThing == "pickaxe"  and (player.getPg() >= 15):
        item = Item("pickaxe", 10,0 ,15)
        player.buy(15)
        player.addItem(item)
                
    elif nameofThing == "angel wings"  and (player.getPg() >= 50):
        item = Item("angel wings", 25, 25, 50)
        player.buy(50)
        player.addItem(item)

# ok searches for item for a specific person
def lookForItemId_rpg(serverPlayers, userID, itemName):
    if(serverPlayers.searchforPlayer(userID) == 0):
        return 0
    else:
        player = serverPlayers.returnPlayer(userID)
        return player.searchPlayerInventory(itemName) 
         
    
# ok searches for item for a specific person
def retrieveItemfromId_rpg(serverPlayers, userID, itemName):
    player = serverPlayers.returnPlayer(userID)
    if(player.searchPlayerInventory(itemName) == 1):
        return player.returnPlayerInventory(itemName)

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
    stickItem = Item("stick", 1, 0, 0)
    player.addItem(stickItem)
    stickItem = Item("card", 0, 0, 10)
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
#   ======================================================================================

#  =========
#  store gen
async def rp_store_gen(interaction: discord.Interaction):

#   choose name
    name_rp = "storeName"
    
#   show store options as well as buttons
    embed = rp_store_show(name_rp)
    view = rp_store_select(interaction)
    await interaction.response.send_message(embed = embed, view= view)
#   ======================================================

#  =======
#    store
def rp_store_show(store_name):
#   create embed
    embed=discord.Embed(title="Welcome to  " + store_name + " store")
    embed.set_image(url="https://m.media-amazon.com/images/I/416CkZQfMFL._AC_.jpg")
    return embed 
#   ============

#  =======
#    store
def rp_store_select(interaction: discord.Interaction):

#   **************************************************************************************************
#   Notes: maybe change store to an entity and do a for loop to get inventory of store like in rp_char
#           will also allow the ability to make different stores and items instead of hard coding items
#   ***************************************************************************************************

#   create embed
    view = View()
    
#   create and add buttons to view 
    button = StoreItem_Button("angel wings")
    view.add_item(button)
    button = StoreItem_Button("streetware")
    view.add_item(button)
    button = StoreItem_Button("card")
    view.add_item(button)
    button = StoreItem_Button("stick")
    view.add_item(button)
    button = StoreItem_Button("pickaxe")
    view.add_item(button)
    button = StoreItem_Button("sell")
    view.add_item(button)
    return view 
#   ===========

#  ===========
#    challenge
async def rp_challenge(interaction: discord.Interaction):
#   create embed
    await rp_challenge_message(interaction); 
    
    #   do u accept or do u not function 
#   after if yes sim batle 
#   else send message declined
#   ===============================================

#  ===========
#    challenge
async def rp_challenge_message(interaction: discord.Interaction):
#   create embed
    embed=discord.Embed(title="Challenged by " + interaction.user.name)
    embed.set_image(url="https://cdn3.iconfinder.com/data/icons/fantasy-1/500/fantasy-01-512.png")

    await interaction.response.send_message(embed=embed); 
#   ===============================================

#  ===========
#    challenge
async def rp_challenge_buttons(interaction: discord.Interaction):
#   do u accept or do u not function 
    view = View()
    await rp_challenge_message(view=view); 
#   ========================================

#   ============
#   message gold
async def rp_message_goldf(message):
#       get user and search for user
        userID = message.author.id 
        if serverPlayers.searchforPlayer(userID) == 0:
            # await message.channel.send('does not exist person' + message.author.name)
            return
#       if found try to give user Gold 
        userChar = serverPlayers.returnPlayer(userID)
        
#       ******************************
#       Notes:
#       to get messages for like a 10 i need to make an array for activyt and add to activity 
#               so i cant just discrod i need to make my own database of user acitivtyt 
#               so will try to implement in the future for now just add gold
#               so features such as delete if user not active 
#               reward for active days in a row etc nneed to be implemented later * maybe just add to user array 
#               but person needs to create char for that to be used so its not default might change features
#       *******************************************************************************************************
        userChar.gainPg(1)
        return
        # await message.channel.send('give gold' + message.author.name)
#       ===============================================================

# fix later already spend an ungodly amount of time
# need to learn how to go thorugh list
# learn how to remove roles from list
# have main logicx down just need to see if syntax exist to let me do what i want 

#   ============
#   update roles 
async def rp_update_roles_function(interaction: discord.Interaction):
    guild = interaction.guild

#   create roles and wont do anything if it already exists
    if  not get(guild.roles, name="stone"):
        await guild.create_role(name="stone")
        await guild.create_role(name="bronze")
        await guild.create_role(name="silver")
        await guild.create_role(name="gold")
        await guild.create_role(name="plat")
    
#   roles 
    role = discord.utils.get(guild.roles, name='stone')
    role1 = discord.utils.get(guild.roles, name='bronze')
    role2 = discord.utils.get(guild.roles, name='silver')
    role3 = discord.utils.get(guild.roles, name='gold')
    role4 = discord.utils.get(guild.roles, name='plat')
    
#   traverse whole list 
    for i in range(0, serverPlayers.getAllPlayersDataSize()):
#   put into proper role
        if (serverPlayers.playerList[i].getPg() > 0) and (serverPlayers.playerList[i].getPg() <= 100):
            await interaction.user.edit(roles=[])
            await interaction.guild._add_role(role,serverPlayers.playerList[i].name )
            continue
        elif (serverPlayers.playerList[i].getPg() > 100) and (serverPlayers.playerList[i].getPg() <= 101):
            await interaction.user.edit(roles=[])
            await interaction.guild._add_role(role,serverPlayers.playerList[i].name )
            continue
        elif (serverPlayers.playerList[i].getPg() > 102) and (serverPlayers.playerList[i].getPg() <= 103):
            await interaction.user.edit(roles=[])
            await interaction.guild._add_role(role,serverPlayers.playerList[i].name )
            continue
        elif (serverPlayers.playerList[i].getPg() > 104) and (serverPlayers.playerList[i].getPg() <= 105):
            await interaction.user.edit(roles=[])
            await interaction.guild._add_role(role,serverPlayers.playerList[i].name )
            continue
        elif (serverPlayers.playerList[i].getPg()) > 106:
            await interaction.guild._remove_role(roles=[])
            await interaction.guild._add_role(role,serverPlayers.playerList[i].name )
            continue
        
    await interaction.response.send_message("kill me soon update ended")
#   ===========================================================

#   try to add to allplayerslist 
def tryInsertADPList(serverPlayersList, a_userName, a_userID):
#       return 1 on fail
        if serverPlayersList.searchforPlayer(a_userID) == 1:
            return 1
#       return 0
        else:
            player= Player(a_userName, a_userID)
            serverPlayersList.addplayertoList(player)
            return 0
        
#   return 1 if valid
#   return 0 if invalid
#   return 2 if same person for specail message
#   might put stricter conditions later so that roles cant farm lower roles
def fight_valid(serverPlayersList, userID1, userID2):
    if userID1 == userID2:
        return 2
    return (serverPlayersList.searchforPlayer(userID1) == 1 and 1 == serverPlayersList.searchforPlayer(userID2))

#   favors challengee (challenger moves second)
#   return 0 when challenger wins 
#   returns 1 when challenger loses
def fight_rpg_sim(challengerHP, challengerAttk, challengeeHP, challengeeAttk):

#   if same char
    if ((challengerHP == challengeeHP) and (challengeeAttk == challengerAttk)):
#       how to generate random number return 0 or 1 half the time 
        return random.randint(0, 1)
     
#   simulate fight
    while (True):
        challengerHP = challengerHP - challengeeAttk
        if(challengerHP <= 0 ):
            return 0
        challengeeHP = challengeeHP - challengerAttk
        if(challengeeHP <= 0 ):
            return 1

def get_totalAttack_char(player1):
#   if no weapon search for weapon 
    if player1.getEquippedSize() == 0 and player1.getInventorySize() == 0:
        return player1.getStrength()
        
    if player1.getEquippedSize() == 0 and player1.getInventorySize() != 0:
        defaultAttackItem = 0
#       search for default item and swap weaker items for it then return total attack
        for i in range(0, player1.getInventorySize()):
            item = player1.getItem(i)
            if(item.getStrengthItem() > defaultAttackItem):
                defaultAttackItem = item.getStrengthItem()     
        return (player1.getStrength()+ defaultAttackItem)

    if player1.getEquippedSize() != 0:
#       go through item list and add up all items to total attack 
        totalAttack = 0
        weaponsCarried = player1.getEquippedSize()
        
#       penalty for carrying more than 5 items no damage increase
        if weaponsCarried >= 5:
            return player1.getStrength()
        
        for i in range(0, weaponsCarried):
            item = player1.getEquippedItem(i)
            totalAttack = totalAttack + item.getStrengthItem()

#       carry penalty 
        # carryPenalty = 1-((1-weaponsCarried)(.25))
        # floatingAttack = totalAttack*carryPenalty
        return player1.getStrength() + (totalAttack - weaponsCarried*5)

def playersColor_rpg(playerName):
    letterQuan = 0#283
    for i in range(len(playerName)):
        letterQuan = letterQuan + ord(playerName[i])
    trueColor = letterQuan % 6 
    
#   options
#   AQUA
    if  trueColor == 0:
        return 1752220
#   DARK_GREEN	
    if  trueColor == 1:
        return 2067276
#   DARK_PURPLE	
    if  trueColor == 2:
        return 7419530
#   GOLD
    if  trueColor == 3:
        return 15844367
#   RED
    if  trueColor == 4:
        return 15158332
#   NAVY	
    if  trueColor == 5:
        return 15158332
#   BLURPLe
    if  trueColor == 6:
        return 15158332
        
#  returns 0 on succsss
#  returns 1 on failure no messages
def clearMsgActivity(player_obj):
    
    if player_obj.getmsgAct() == 0:
        return 1
    else:
        player_obj.clearMsgHist()
        return 0
    
# return 0 if added to inacitivty count
# return 1 if deleted
def manageInactivePlayers(player_obj):
        
    if player_obj.getinActive_warningS() == 0:
        player_obj.addtoIA()
        return 0
    else:
        # delete character function plus messaging and sending stuff 
        return 1 
    
def deletekickmsg_rpg(interaction: discord.Interaction, serverPlayers , rpg_userID):
#   calls delete char: remove from list 
    if serverPlayers.manageInactivePlayers(rpg_userID) == 0:
            user = interaction.guild.get_member(rpg_userID)
            #send mesage to discord aka the one who called the interaction
            interaction.send(embed=getDeathEmbed())
            
            #send message to kicked person
            user.send(embed=getDeathEmbed(112233))
            user.kick(reason=None)
#   send message to killed bot
    interaction.send("failed to delete: " + rpg_userID)
 
#  return -1 list empty 
#  return number of people deleted 
#  return 0 success
def cleanup_msgActivity_AllUsers(interaction: discord.Interaction, ServerList):
    # if empty return 0 
    i = serverPlayers.getAllPlayersDataSize() 
    if i == 0:
        return -1
    
    noInactivePlayers  = 0 
    
    for i in  range(serverPlayers.getAllPlayersDataSize()):
        tempPlayer = serverPlayers.getPlayerat_loc(i)
        userID = tempPlayer.getUserID()
#       if 1 ie empty
        if clearMsgActivity(tempPlayer): 
#           add to total deleted players if plater deleted/kicked and send msg to player 
            if manageInactivePlayers(tempPlayer):
                deletekickmsg_rpg(interaction, serverPlayers , userID)
                noInactivePlayers = noInactivePlayers + 1
    
    return noInactivePlayers

# could later mod to send stats of char at time of death 
def getDeathEmbed(color_num):
    embed=discord.Embed(title="Due to inactivity you have been killed off and kicked from server", color=color_num)
    embed.set_image()#sqaure
    return embed

#send message
def death_message_rpg():
    embed=discord.Embed(title="left to a worse place...",description="comraded blah")
    embed.set_image()#skull
    return embed


#  clears message on time 00::00::00 call it to act on this time 
#  calls clearMsgActivity_AllUsers()
async def clearDaily_rpg(interaction: discord.Interaction):
#  The cron trigger works w/ wall clock
#  apscheduler.triggers.cron
#  schedule jobs to be executed in the futur
#   initializing scheduler
    scheduler =  AsyncIOScheduler()# comes from apscheduler 

#   sends so add job and set the time to 00:00:00/  pass in function to do as first arguemnet
    scheduler.add_job(cleanup_msgActivity_AllUsers(interaction, serverPlayers), 'cron', hour=0, minute=00) 
    
#   run scheduler
    scheduler.start()


# #have to fix roles in python demotiion and promotion

# #so how to get enemies id ok we just cheat grab  thier id and send it to that
def sendChallengetoOpponent(interaction: discord.Interaction, rpg_userID, nameChallenger):
    user = interaction.guild.get_member(rpg_userID)
#   create a view and some buttons to accept or reject  maybe time period or something and dusaper or diable afterwards
    view = discord.ui.View(timeout=None)
    buttonYes =  discord.ui.Button(label="Yes")
    buttonNo =  discord.ui.Button(label="No")
    buttonNo.callback = no_callback
    buttonYes.callback = yes_callback
    
    view.add_item(buttonYes)
    view.add_item(buttonNo)
    
    embed=discord.Embed(title="Challenged by " + nameChallenger)
    embed.set_image()#swords
    
    
    #make button to time out burnout daammit 
    user.send(view=view, embed=embed)
#   return response 

#use callback to sim battle i spose 
def yes_callback(interaction):
    print("yes")
#send nothing ithink
def no_callback(interaction):
    print("no")

def fight_rpg(serverPlayers, player1, player2):
    serverPlayers  
    player1
    player2
#   call from player obj 
#   call from item exists
#   check they exist 
#   call from get_totalAttack_char
#   so test waepon exists and grab it 
#   then call fight sim and insert bariable 
#   return -1 if error in this case no way for it toi work so default to errro for now
    return -1

# Johnsons
# Construction Safety Gear
# TrackSuit 
# 
# Boost Defense// D1

# Ring
# AngelWings //gives priority Speed D15 
# Halo	     // covers user in a holy light D 20
# Boost Defense++// D5

# Jean
# Hammer Tool//Atk 5
# Sword // Atk 7
# Stick// Atk */
# Boost Attack// D1

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

#   just to help organize
def storeItemsresponses(nameofThing, buyersWalletSize):
#       else check all item options as well as if user has enough gold 
    if nameofThing == "stick" and (buyersWalletSize  >= 1):
            response_to_Buyer = "You have successfully bought " + nameofThing
            
    elif nameofThing == "card" and (buyersWalletSize >= 5):
            response_to_Buyer = "You have successfully bought " + nameofThing
    
    elif nameofThing == "streetware" and (buyersWalletSize >= 30):
            response_to_Buyer = "You have successfully bought " + nameofThing
               
    elif nameofThing == "pickaxe"  and (buyersWalletSize>= 15):
            response_to_Buyer = "You have successfully bought " + nameofThing
                
    elif nameofThing == "angel wings"  and (buyersWalletSize >= 50):
            response_to_Buyer = "You have successfully bought " + nameofThing
            
    else:
        response_to_Buyer = "You are a broke and failed to buy a " + nameofThing
            
    return response_to_Buyer

def storeItemsInteractionWithBuyer(player, nameofThing):
#   do stuff to buyer 
    if nameofThing == "stick" and (player.getPg()  >= 1):
        item = Item("stick", 1, 0, 1)
        player.buy(1)
        player.addItem(item)
            
    elif nameofThing == "card" and (player.getPg() >= 5):
        item = Item("card", 1, 2, 5)
        player.buy(5)
        player.addItem(item)
    
    elif nameofThing== "streetware" and (player.getPg() >= 30):
        item = Item("streetware", 10, 30 , 30)
        player.buy(30)
        player.addItem(item)
               
    elif nameofThing == "pickaxe"  and (player.getPg() >= 15):
        item = Item("pickaxe", 10,0 ,15)
        player.buy(15)
        player.addItem(item)
                
    elif nameofThing == "angel wings"  and (player.getPg() >= 50):
        item = Item("angel wings", 25, 25, 50)
        player.buy(50)
        player.addItem(item)

# ok searches for item for a specific person
def lookForItemId_rpg(serverPlayers, userID, itemName):
    if(serverPlayers.searchforPlayer(userID) == 0):
        return 0
    else:
        player = serverPlayers.returnPlayer(userID)
        return player.searchPlayerInventory(itemName) 
         
    
# ok searches for item for a specific person
def retrieveItemfromId_rpg(serverPlayers, userID, itemName):
    player = serverPlayers.returnPlayer(userID)
    if(player.searchPlayerInventory(itemName) == 1):
        return player.returnPlayerInventory(itemName)

