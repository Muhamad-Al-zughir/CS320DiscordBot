# shbang

# 3/22/23
# Shawyan Tabari
# Testing suite for various elements of CS 320 Discord bot project

# Note: I decided to make a variety of tests for different codebases of our Discord Bot Project.
#       These test include functions from Libgen, Botgame, and muzique
#       These files have been included as a copy in a test folder to preserve the working github repository

# Note: I could not include many of my own asynchronous functions from the music bot
#       As they proved to be extremely difficult to develop tests for, due to connecting to the multiple APIS
#       initializing a discord bot instance for each test, and simulating (mocking) the objects needed
#       to make the functions to work. 

#       This is why I have decided to test my partners aspects of the discord bot mainly, as
#       theirs proved much easier to test. I have made sure to the best of my ability to keep my tests
#       unique and independent from theirs.

from games import *
import lib as libby
from muzique import *
import pytest


# 1. Acceptance Test / Black Box
# Attempts to search for a Book author with Libgen with an invalid language 
def test_LibbyWrongLang_auth():                 # Wrong Language Search for LibGen - Author
    authquery = "理查德戴利"                     # Give it wrong language
    query = "author"                            # Specify author and perform operation
    results = libby.basicSearch(query, authquery)
    assert len(results) == 0                    # Assert no results found



# 2. Acceptance Test / Black Box
# Attempts to search for a Book title with Libgen with an invalid language 
def test_LibbWrongLang_title():                 # Wrong Language Search for Libgen - Title
    titlequery = "政治、种族和芝加哥的治理"       # Give it wrong language
    query = "title"                             # Specify title and perform operation
    results = libby.basicSearch(query,titlequery)
    assert len(results) == 0                    # Assert no results found



# 3. Branch Coverage / White Box testing  
#    Focus of Branch Coverage / White box test beow
"""
def lookForItemId_rpg(serverPlayers, userID, itemName):
    if(serverPlayers.searchforPlayer(userID) == 0):
        return 0
    else:
        player = serverPlayers.returnPlayer(userID)
        return player.searchPlayerInventory(itemName)
"""
# Searches for all players in player list using an ID, and checks players inventory for a given item
# As this is a whitebox test, all cases for the provided function will be exhausted
def test_GamesLookingForLoot_ValidItem():       # Search for a valid player item
    newPlayer = Player("Johnathan", 42069)      # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)    # New Player added to List
    newPlayer.addItem(Item("Mccarthy",strength = 0,defense = 0,pg = 0))            # Add Item to player bag
    returnVal1 = lookForItemId_rpg(serverPlayers,42069,"Mccarthy")                 # Search for Valid item

    assert(returnVal1 == 1)                     # Item is in player inventory
                   
                                                # Invalid Player Item
    newPlayer = Player("Richard", 11206)        # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)    # New Player added to List
    newPlayer.addItem(Item("illegalWeapon",strength = 50,defense = 25,pg = 1))     # Add Item to player bag
    returnVal2 = lookForItemId_rpg(serverPlayers,11206,"legalWeapon")              # Search for Valid item
    
    assert(returnVal2 == 0)                     # Item is not in player inventory


                                                # Invalid Player (Not in list)                        
    newPlayer = Player("Band", 90210)           # New Player instantiated 
                                                # Notice: New player NOT added to list
    newPlayer.addItem(Item("Justice",strength = 12,defense = 25,pg = 5))           # Add Item to player bag
    returnVal3 = lookForItemId_rpg(serverPlayers,90210,"Justice")                  # Search for Valid item

    assert(returnVal3 == 0)                     # Player is not in list



#4. Acceptance Test / Black Box
# Tests store responses given a satisfactory wallet size and an valid item query
def test_validResponses():                                                         # Repeat Procedure for each Game Item:
    validItems = ["stick","card","streetware","pickaxe","angel wings"]             # Predetermine valid list of items
    walletNum = 0                                                                  # Set initial wallet size
    for items in validItems:                                                       # Iterate through list for valid items
        if items == "stick":                                                        
            walletNum = 2                                                          # Reset to valid wallet size and call function
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You have successfully bought " + items)         # Assert function returns successful response message
        elif items == "card":
            walletNum = 6
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You have successfully bought " + items)
        elif items == "streetware":
            walletNum = 31
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You have successfully bought " + items)
        elif items == "pickaxe":
            walletNum = 16
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You have successfully bought " + items)
        elif items == "angel wings":
            walletNum = 51
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You have successfully bought " + items)


#5. Acceptance Test / Black Box
# Tests store responses given an Invalid wallet size and an valid item query
def test_validItemsInsufficientFunds():                                            # Repeat Procedure for each game Item:
    validItems = ["stick","card","streetware","pickaxe","angel wings"]             # Predetermine list of valid items
    walletNum = 0                                                                  # Set initial wallet size
    for items in validItems:                                                       # Iterate through list, do not reset wallet value
        if items == "stick":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)  # Check for Invalid Funds response due to low wallet num
        elif items == "card":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "streetware":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "pickaxe":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "angel wings":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)


#6. Acceptance Test / Black Box
# Tests store responses given a satisfactory wallet size and an invalid item query
def test_invalidItems():                                                           # Repeat Procedure for each game Item:
    invalidItems = ["bigweapon","Justice","Pan","Pike","boots"]                    # Predetermine list of invalid items (tbd if implemented later)
    walletNum = 1000                                                               # Set initial wallet num to 1000 (high funds)
    for items in invalidItems:                                                     # Iterate through invalid items and attempt to buy
        if items == "bigweapon":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)  # Check for invalid response due to invalid item (need to alter response in future)
        elif items == "Justice":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "Pan":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "Pike":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)
        elif items == "boots":
            returnval = storeItemsresponses(items,walletNum)
            assert (returnval ==  "You are a broke and failed to buy a " + items)

#7. Integration Testing
# Big Bang Testing
# Uses Server List, Item List, and Player list classes
# Attempts to retrieve new item value from created player
def test_itemRetrieval_success():
    newPlayer = Player("Guys", 10)              # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)    # New Player added to List
    
    newPlayer.addItem(Item("Poison",strength = 1000,defense = 2,pg = 7))            # Add Item to player bag
    newPlayer.addItem(Item("bigHelmet",strength = 2,defense = 100,pg = 5))

    returnVal1 = retrieveItemfromId_rpg(serverPlayers,10,"bigHelmet")
    assert(returnVal1.name == "bigHelmet")
    assert(returnVal1.strength == 2)
    assert(returnVal1.defense == 100)
    assert(returnVal1.pg == 5)

    returnVal2 = retrieveItemfromId_rpg(serverPlayers,10,"Poison")
    assert(returnVal2.name == "Poison")
    assert(returnVal2.strength == 1000)
    assert(returnVal2.defense == 2)
    assert(returnVal2.pg == 7)

#8. Integration Testing
# Big Bang Testing
# Uses Server List, Item List, and Player list classes
# Attempts to retrieve item with invalid player ID
def test_itemRetrieval_failure():
    newPlayer = Player("Jersey", 50)            # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)    # New Player added to List
    
    newPlayer.addItem(Item("Uzi",strength = 500,defense = 0,pg = 50))            # Add Items to player bag
    newPlayer.addItem(Item("Cape",strength = 2,defense = 100,pg = 5))

    with pytest.raises(Exception):                                               # Checks for exception due to invalid player ID
        returnVal1 = retrieveItemfromId_rpg(serverPlayers,50241,"Uzi")             
        returnVal2 = retrieveItemfromId_rpg(serverPlayers,50241,"Cape")
    

# 9. Acceptance Test / Black Box
# Attempts to purchase stick from the game shop with sufficient funds
def test_merchantInteraction_validStick():
    newPlayer = Player("Morty", 13)                 # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 2                              
    storeItemsInteractionWithBuyer(newPlayer, "stick")      # Call upon Merchant interaction function to buy stick
    newItemobj = newPlayer.searchPlayerInventory("stick")   # Check if stick is found in inventory (int)
    newItemStatus = newPlayer.returnPlayerInventory("stick")# Check if stick attributes can be determined

    assert (newPlayer.searchPlayerInventory("stick") == 1)  # Assert stick attributes below
    assert(newItemStatus.name == "stick")
    assert(newItemStatus.strength == 1)
    assert(newItemStatus.defense == 0)
    assert(newItemStatus.pg == 1)

# 10. Acceptance Test / Black Box
# Attempts to purchase Stick from the game shop with insufficient funds
def test_merchantInteraction_InvalidStick():
    newPlayer = Player("Morty", 13)                 # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 0
    with pytest.raises(ValueError):                 # Attempting to buy stick with invalid funds, check for exception            
        storeItemsInteractionWithBuyer(newPlayer, "stick")



# 11. Acceptance Test / Black Box
# Attempts to purchase Card from the game shop with sufficient funds
def test_merchantInteraction_validCard():
    newPlayer = Player("Rickard", 24)               # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such

    newPlayer.pg = 6                              
    storeItemsInteractionWithBuyer(newPlayer, "card")       # Call upon Merchant interaction function to buy card
    newItemobj = newPlayer.searchPlayerInventory("card")    # Check if card is found in inventory (int)
    newItemStatus = newPlayer.returnPlayerInventory("card") # Check if card attributes can be found 

    assert (newPlayer.searchPlayerInventory("card") == 1)   # Assert card attributes below
    assert(newItemStatus.name == "card")
    assert(newItemStatus.strength == 1)
    assert(newItemStatus.defense == 2)
    assert(newItemStatus.pg == 5)


# 12. Acceptance Test / Black Box
# Attempts to purchase card from the game shop with insufficient funds
def test_merchantInteraction_InvalidCard():
    newPlayer = Player("Rickard", 24)               # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 4
    with pytest.raises(ValueError):                 # Attempting to buy card with insufficient funds, check for exception             
        storeItemsInteractionWithBuyer(newPlayer, "card")


# 13. Acceptance Test / Black Box
# Attempts to purchase streetware from the game shop with sufficient funds
def test_merchantInteraction_validStreetware():
    newPlayer = Player("Bruh", 5192)                # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such

    newPlayer.pg = 31                              
    storeItemsInteractionWithBuyer(newPlayer, "streetware")       # Call upon merchant function to buy streetware
    newItemobj = newPlayer.searchPlayerInventory("streetware")    # Check streetware is in inventory (int)
    newItemStatus = newPlayer.returnPlayerInventory("streetware") # Check for streetware attributes and assert below

    assert (newPlayer.searchPlayerInventory("streetware") == 1)
    assert(newItemStatus.name == "streetware")
    assert(newItemStatus.strength == 10)
    assert(newItemStatus.defense == 30)
    assert(newItemStatus.pg == 30)


# 14. Acceptance Test / Black Box
# Attempts to purchase streetware from the game shop with insufficient funds
def test_merchantInteraction_InvalidStreetware():
    newPlayer = Player("Bruh", 5192)                # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 29
    with pytest.raises(ValueError):                 # Attempting to buy streetware with insufficient funds, check for Error             
        storeItemsInteractionWithBuyer(newPlayer, "streetware")


# 15. Acceptance Test / Black Box
# Attempts to purchase pickaxe from the game shop with sufficient funds
def test_merchantInteraction_validPickaxe():
    newPlayer = Player("Mortimer", 421243)          # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such

    newPlayer.pg = 16                              
    storeItemsInteractionWithBuyer(newPlayer, "pickaxe")       # Call upon merchant to buy pickaxe item
    newItemobj = newPlayer.searchPlayerInventory("pickaxe")    # check if pickaxe item is in inventory (int)
    newItemStatus = newPlayer.returnPlayerInventory("pickaxe") # Recieve pickaxe item attributes 

    assert (newPlayer.searchPlayerInventory("pickaxe") == 1)  # Assert attributes and found status below 
    assert(newItemStatus.name == "pickaxe")
    assert(newItemStatus.strength == 10)
    assert(newItemStatus.defense == 0)
    assert(newItemStatus.pg == 15)


# 16. Acceptance Test / Black Box
# Attempts to purchase Pickaxe from the game shop with insufficient funds
def test_merchantInteraction_InvalidPickaxe():
    newPlayer = Player("Mortimer", 421243)          # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 14
    with pytest.raises(ValueError):                 # Attempting to buy Pickaxe with insufficient funds, check for exception             
        storeItemsInteractionWithBuyer(newPlayer, "pickaxe")


# 17. Acceptance Test / Black Box
# Attempts to purchase Angel wings from the game shop with sufficient funds
def test_merchantInteraction_validAngel():
    newPlayer = Player("Sean", 123)                 # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such

    newPlayer.pg = 51                              
    storeItemsInteractionWithBuyer(newPlayer, "angel wings")       # Call upon merchant to purchase item
    newItemobj = newPlayer.searchPlayerInventory("angel wings")    # Check that angel wings item is in inventory
    newItemStatus = newPlayer.returnPlayerInventory("angel wings") # Check that Angel wings attributes are determined

    assert (newPlayer.searchPlayerInventory("angel wings") == 1)   # Assert angel wings values below
    assert(newItemStatus.name == "angel wings")
    assert(newItemStatus.strength == 25)
    assert(newItemStatus.defense == 25)
    assert(newItemStatus.pg == 50)


# 18. Acceptance Test / Black Box
# Attempts to purchase Angel wings from the game shop with insufficient funds
def test_merchantInteraction_InvalidAngel():
    newPlayer = Player("Sean", 123)                 # New Player instantiated
    serverPlayers.addplayertoList(newPlayer)        # New Player added to List)
                                                    # if in for inventory # search player inventory
                                                    # item name, strength, defense, pg check if it is as such
    newPlayer.pg = 49                               
    with pytest.raises(ValueError):                 # Trying to buy angel wings with insufficient funds, check for exception     
        storeItemsInteractionWithBuyer(newPlayer, "angel wings")


# 19. Acceptance Test / Black Box
# Strips given YouTube title of bad characters
def test_titleStrip():                              # Predetermine preset list of YouTube Songs 
    titles = ["Juice WRLD - Bandit ft. NBA Youngboy (Directed by Cole Bennett)",
              "POP SMOKE - WELCOME TO THE PARTY [SHOT BY GoddyGoddy]",
              "Y.MStizzy - G.M.D.W.T.S [official music video]",
              "Cochise - Tell Em ft. $NOT (Directed by Cole Bennett)",
              "Polo G - RAPSTAR (Official Video)",
              "A$AP Rocky-1 Train ft Kendrick Lamar,Joey Bada$$,YelaWolf, Danny Brown, Action Bronson & Big K.R.I.T"]
    
    for title in titles:                            # Iterate list and call upon filterTitle to strip bad characters
        testTitle = filterTitle(title)              # Assert no bad characters present in title
        assert("[" not in testTitle)
        assert("(" not in testTitle)
        assert("ft" not in testTitle)
        assert("ft." not in testTitle)
        assert("feat." not in testTitle)
        assert("feat" not in testTitle)
        assert("featuring" not in testTitle)


# 20. Acceptance Test / Black Box
# Process a formatted YouTube video date
def test_DateProcessMonth():                       # Predetermine preset list of Dates
    testDates = ["20200406","20060502","20121221", "20130605",
                 "20220115", "20211017"]
                                                   # Predetermine preset list of Months
    testMonths = ['January', 'February', 'March', 'April',
                    'May', 'June', 'July', 'August',
                    'September', 'October', 'November', 'December']
    
    for dates in testDates:                         # Iterate Call upon process month function 
        newMonth = processMonth(dates)
        assert(newMonth in testMonths)              # Assert it is in list of valid months


# 21. Acceptance Test / Black Box
# Process a formatted YouTube video year
def test_DateProcessYear():                         # Predetermine preset list of Dates
    testDates = ["20231206","20060420","20090504", "20221017",
                 "20000502", "20221119"]
    
    testYears = ['2000', '2001', '2002', '2003',    # Predetermine preset list of Years
                    '2004', '2005', '2006', '2007',
                    '2008', '2009', '2010', '2011',
                    '2012', '2013', '2014', '2015', 
                    '2016','2017', '2018', '2019', 
                    '2020', '2021', '2022','2023']


    for dates in testDates:                         # Iterate date list and Call upon process month function
        newYear = processYear(dates)
        assert(newYear in testYears)                # Assert that a valid year has been returned

# 22. Acceptance Test / Black Box
# Process a formatted YouTube video Day
def test_DateProcessDay():                          # Predetermine preset list of Dates
    testDates = ["20170608","20171209","20040115", "20160207",
                 "20191209", "20200317"]
                                                    # Pretermine preset list of days
    testDays = ['01', '02','03', '04', '05', '06', '07', '08', '09', '10',
                '11', '12','13', '14', '15', '16', '17', '18', '19', '20',
                '21', '22','23', '24', '25', '26', '27', '28', '29', '30',
                '31']

    for dates in testDates:                         # Iterate through and process dates
        newDay = processDay(dates)
        assert(newDay in testDays)                  # Assert that a valid date has been received

