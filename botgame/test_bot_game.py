from game import *
from unittest.mock import Mock
#tests contains asserts
#blackbox testing == acceptance tests
#whitebox test, past function as comment above it 
#integration test, tests 2 units comments units tested/approach/unit can == class

#acceptance test

#white box testing
#function

#integration testing


#10
#create character object with name and id 
#delete character object with id 
#every message increases one gold less than 10
#wont let two people with same id create
#resultfight function returns who dies first depending on health and damage
#call fight function when list cant find players dont return 
#what happens if both characters are equal do coin toss and test rng 
#store items bought goes up when item bought
# store creation creates store with item
# store upgragdes repuation and changes namee when rank changes

#tests that proper role gets upgraded with enough money role
#tests that proper role gets upgraded with enough money role 1 
#tests that proper role gets upgraded with enough money role 2
#tests that proper role gets upgraded with enough money role 3

#11
#white box testing for selling if item exists if no item exists or if item is not sellable

#12
#integratino testing buying 3 classes Store, Items, and Character

#1 create character object with name being name and key being discords id number // cann only be accesed with userID
# acceptance tests
def test_create_char():
    name = "John"
    userID = 112233
    serverCharacter = Player(name, userID)
    assert (serverCharacter.getName() == "John" and serverCharacter.getUserID() == 112233)
    
#   ADP

#2 returns 1, same id insert into list
# acceptance tests
def test_Insert_duplicate_IDS():
#   set up
    mockdup_userID = 112233
    tryInsertADPList(serverPlayers, "Person1", mockdup_userID)

#   check to see if it return error ie 1    
    assert (tryInsertADPList(serverPlayers, "Person2", mockdup_userID)  == 1)

#3 returns 0, the same name but different IDS
# acceptance tests
def test_Insert_duplicate_Name():
#   set up
    mockdup_userName = "John"
    tryInsertADPList(serverPlayers, mockdup_userName, 112235)
    
    assert (tryInsertADPList(serverPlayers, mockdup_userName, 112234)  == 0)
    
#4 see that added succesfully two to the list of players
# acceptance tests
def test_Insert_ADP_size():
#   set up
    originalSize = serverPlayers.getAllPlayersDataSize()
    tryInsertADPList(serverPlayers, "Person1", 112238)
    errorReturn = tryInsertADPList(serverPlayers, "Person1", 112239)

#   check to see if it return error is 0 and size is +2 of originald
    assert (errorReturn == 0 and serverPlayers.getAllPlayersDataSize() == originalSize+2) 
    
#   fightvalid
     
#5 returns 1, the two players made and exist in serverPlayers(an array of player objects)
# acceptance tests
def test_two_people_can_fight_two_exists():
#   set up
    player1 = Player("John", 1122)
    player2 = Player("Jane", 11223)
    serverPlayers.addplayertoList(player1)
    serverPlayers.addplayertoList(player2)
    
    assert (fight_valid(serverPlayers, 1122, 11223) == 1)
    
#6 see if returns 0, fight not allowed
# acceptance tests
def test_two_people_can_fight_one_exists():
#   set up
    userID2 = 121212
    player1 = Player("Rob1", 11220)
    serverPlayers.addplayertoList(player1)
    
    assert (fight_valid(serverPlayers, 11220, userID2) == 0)
    
#7 returns 2, when tries to fight self
# acceptance tests
def test_two_people_can_fight_self():
#   set up 
    player1 = Player("Rob1", 11220)
    serverPlayers.addplayertoList(player1)
    
    assert (fight_valid(serverPlayers, 11220, 11220) == 2)
#   fight similuate

#8 challenger wins return 1
#   acceptance tests
def test_fightsim_challenger_win():
    challengerWin = fight_rpg_sim(100, 35, 100, 20)
#   set up 
    assert (challengerWin==1)

#9 challengee wins return 0
#   acceptance tests
def test_fightsim_challengee_win():
    challengerWin = fight_rpg_sim(100, 20, 200, 20)
#   set up 
    assert (challengerWin==0)
    
#10 challenger and challengee return 0
#   acceptance tests 
def test_fightsim_challenger_w():
    challengerWin = fight_rpg_sim(100, 25, 100, 25)
#   set up 
    assert (challengerWin==0)
  
#   WHITEBOX TESTING
# def get_totalAttack_char(player1):
# #   if no weapon search for weapon 
#     if player1.getEquippedSize() == 0 and player1.getInventorySize() == 0:
#         return player1.getStrength()
        
#     if player1.getEquippedSize() == 0 and player1.getInventorySize() != 0:
#         defaultAttackItem = 0
# #       search for default item and swap weaker items for it then return total attack
#         for i in range(0, player1.getInventorySize()):
#             item = player1.getItem(i)
#             if(item.getStrengthItem() > defaultAttackItem):
#                 defaultAttackItem = item.getStrengthItem()     
#         return (player1.getStrength()+ defaultAttackItem)

#     if player1.getEquippedSize() != 0:
# #       go through item list and add up all items to total attack 
#         totalAttack = 0
#         weaponsCarried = player1.getEquippedSize()
        
# #       penalty for carrying more than 5 items no damage increase
#         if weaponsCarried >= 5:
#             return player1.getStrength()
        
#         for i in range(0, weaponsCarried):
#             item = player1.getEquippedItem(i)
#             totalAttack = totalAttack + item.getStrengthItem()

# #       carry penalty 
#         # carryPenalty = 1-((1-weaponsCarried)(.25))
#         # floatingAttack = totalAttack*carryPenalty
#         return player1.getStrength() + (totalAttack - weaponsCarried*5)    

#11 challenger and challengee return 0
#   acceptance tests 
def test_weapon_exists_add_else_default():
    player1 = Player("name1", 11000)
    player2 = Player("name2", 11001)
    player3 = Player("name3", 11002)
    player4 = Player("name4", 11003)    
    player5 = Player("name5", 11004)
    player6 = Player("name6", 11006)    
    itemWeak = Item("name", strength=1, defense=0, pg=0)
    itemStrongest = Item("name", strength=4, defense=0, pg=0)
  
#   Case Equipped 6
    for i in range (6): 
        player1.equipItem(itemWeak)
    assert(get_totalAttack_char(player1) == player1.getStrength())    
   
#   Case Equipped 5
    for i in range (5): 
        player2.equipItem(itemWeak)
    assert(get_totalAttack_char(player2) == player2.getStrength())    
    
#   Case Equipped 2
    for i in range (2): 
        player3.equipItem(itemWeak)
    assert(get_totalAttack_char(player3) == player3.getStrength() + (2-(2*5)))  

#   Case Equipped 0 and invenotory 0
    assert(get_totalAttack_char(player4) == player4.getInventorySize())
    
#   Case Equipped 0 and invenotory not 0 AND 3 items
    player5.addItem(itemWeak)
    player5.addItem(itemWeak)
    player5.addItem(itemStrongest)
    assert(get_totalAttack_char(player5) == player5.getStrength()+4)
    
#   Case Equipped 0 and invenotory not 0 and 1 item
    player6.addItem(itemWeak)
    assert(get_totalAttack_char(player6) == player6.getStrength()+1)
    
#12 acceptance testing 
def test_PlayersColor_rpg():
    name = "Red"

#   DARK_GREEN 0x1F8B4C
    assert(0x1F8B4C == playersColor_rpg(name))



    
