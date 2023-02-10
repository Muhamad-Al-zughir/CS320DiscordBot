import os

import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord.ui import Select, View

#   ============
#   Player class
class Player:
    def __init__(self, nameUser):
        self.name = nameUser
        self.pg =0
        self.hitpoints = 1 
        self.strength = 0 
        self.defense = 0  
        self.inventory = []
        
    def showSelf(self):
        return (self.name + "\n" 
                "hp: " + str(self.hitpoints) + "\n" 
                "strength: " + str(self.strength) + "\n" 
                "defense: " + str(self.defense)
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
        print(len(self.inventory))
        
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
    def returnPlayer(self, name):
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].name == name):
                return self.playerList[i]
#   search for player
    def searchforPlayer(self, name):
        for i in range(0, len(self.playerList)):
            if(self.playerList[i].name == name):
                return 1
        return 0
            
#   add player to list
    def addplayertoList(self, player):
        self.playerList.append(player)
#   ==================================


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
def store():
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

# player creation
player = Player("bob")
print(player.showSelf())
player.showInventory()

# item creation
stickItem = Item("stick", 1, 0)
player.addItem(stickItem)
player.showInventory()

# Serverdata creation
serverPlayers = AllPlayersData()
if(serverPlayers.searchforPlayer("bob") == 0):
    print("not found player ")
    
serverPlayers.addplayertoList(player)

if(serverPlayers.searchforPlayer("bob") == 1):
    print("found player")
    
# store function
store()
print("\nmade it to end\n")