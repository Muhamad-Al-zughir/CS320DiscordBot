from game import *
import pytest
from unittest.mock import Mock

# ==============================================
#   CS Student: Joe Hernandez Lopez
#   Date: 3/24/2023
#   UnitTesting 
#  
#   Notes:
        #tests contains asserts
        #blackbox testing == acceptance tests
        #whitebox test, past function as comment above it 
        #integration test, tests 2 units comments units tested/approach/unit can == class
# =======================================================================================

#1 create character object with name being name and key being discords id number and get those with get functions
# acceptance tests
def test_create_char():
    name = "John"
    userID = 112233
    
    serverCharacter = Player(name, userID)    
    returnedName = serverCharacter.getName()
    returnedUserID = serverCharacter.getUserID()
    assert (returnedName == "John" and returnedUserID == 112233)

#2 returns 1, Same id inserting into list
# acceptance tests
def test_Insert_duplicate_IDS():
#   set up
    mockdup_userID = 112233
    tryInsertADPList(serverPlayers, "Person1", mockdup_userID)

#   check to see if it return error ie 1
    returnedScenerio2 = tryInsertADPList(serverPlayers, "Person2", mockdup_userID)
    assert ( returnedScenerio2 == 1)

#3 returns 0, the same name but different IDS
# acceptance tests
def test_Insert_duplicate_Name():
#   set up
    mockdup_userName = "John"
    
    tryInsertADPList(serverPlayers, mockdup_userName, 112235)
    returnedScenario3 = tryInsertADPList(serverPlayers, mockdup_userName, 112234)
    assert (returnedScenario3 == 0)
    
#4 see that the function succesfully added 3 obj to the list of players
#  bsaicallyy list grows by 3
# acceptance tests
def test_Insert_succesllyaddedtoList():
#   use pythons lens to get original size
    originalSize = serverPlayers.getAllPlayersDataSize()
    
 #   insert and getSize   
    tryInsertADPList(serverPlayers, "Person1", 112238)
    tryInsertADPList(serverPlayers, "Person2", 1122420)
    tryInsertADPList(serverPlayers, "Person3", 112239)
    theListSize = serverPlayers.getAllPlayersDataSize()

#   check to see if it list has grown by 3
    assert (theListSize == originalSize+3) 
    
     
#5 returns 1, it is possible for those players to fight 
# acceptance tests
def test_two_people_can_fight_two_exists():
#   set up
    player1 = Player("John", 1122122)
    player2 = Player("Jane", 11223)
    serverPlayers.addplayertoList(player1)
    serverPlayers.addplayertoList(player2)

    isValidFight = fight_valid(serverPlayers, 1122122, 11223)
    assert (isValidFight == 1)
    
#6 see if returns 0, fight not allowed second person doesnt exist
# acceptance tests
def test_two_people_can_fight_one_exists():
#   set up
    userID2 = 121212
    player1 = Player("Rob1", 1122009)
    serverPlayers.addplayertoList(player1)
    
    isValidFight = fight_valid(serverPlayers, 1122009, userID2)
    assert (isValidFight == 0)
    
#7 returns 2, when tries to fight self Note** user is known through userID number
# acceptance tests
def test_two_people_can_fight_self():
#   set up 
    userID =  11220
    player1 = Player("Rob1", userID)
    serverPlayers.addplayertoList(player1)
    
    isValidFight = fight_valid(serverPlayers, userID, userID)
    assert (isValidFight == 2)
   
#8  challenger wins with these numbner return 1
#   acceptance tests
def test_fight_rpg_sim_challenger_win():
#   fight_rpg_sim(challneger HP, challneger attack, challengee HP,challenee attack )                     
    challengerWin = fight_rpg_sim(100, 35, 100, 20)
#   set up 
    assert (challengerWin==1)

#9 challengee wins with these numbers return 0
#   acceptance tests
def test_fight_rpg_sim_challengee_win():
    challengerWin = fight_rpg_sim(100,15, 200, 15)
#   set up 
    assert (challengerWin==0)
    
#10 challenger and challengee same vals return 0
#   acceptance tests 
def test_fightsim_challenger_w():
    challengerWin = fight_rpg_sim(50, 25, 50, 25)
#   set up 
    assert (challengerWin==random.randint(0, 1))
  
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

#11 white box testing branching coverage
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
    case0Return = get_totalAttack_char(player1)
    player1str = player1.getStrength()
    assert(case0Return == player1str)    
   
#   Case Equipped 5
    for i in range (5): 
        player2.equipItem(itemWeak)
    case1Return = get_totalAttack_char(player2) 
    player2str = player2.getStrength()
    
    assert(case1Return == player2str)    
    
#   Case Equipped 2
    StrengthModder  =  (2-(2*5))

    for i in range (2): 
        player3.equipItem(itemWeak)
    case3Return = get_totalAttack_char(player3) 
    player3str = player3.getStrength()
    
    assert(case3Return == player3str + StrengthModder)  

#   Case Equipped 0 and invenotory 0
    case4Return = get_totalAttack_char(player4) 
    player4str = player4.getStrength()
    
    assert(case4Return == player4str)
    
#   Case Equipped 0 and invenotory not 0 AND 3 items and has to swap items
    player5.addItem(itemWeak)
    player5.addItem(itemWeak)
    player5.addItem(itemStrongest)
    case5Return = get_totalAttack_char(player5) 
    player5str = player5.getStrength()
    
    assert(case5Return == player5str+4)# its +4 because stronges item has +4 attack
    
#   Case Equipped 0 and invenotory not 0 and 1 item and does not have to swap items
    player6.addItem(itemWeak)
    case6Return = get_totalAttack_char(player6) 
    player6str = player6.getStrength()
    assert(case6Return == player6str+1)# its +1 because waek item has +1
    
#12 acceptance testing 
def test_PlayersColor_rpg():
    name = "Red"
    returnValueColor =  playersColor_rpg(name)
#   DARK_GREEN 0x1F8B4C
    assert(0x1F8B4C == returnValueColor )

#15 acceptance testing 
def test_PlayersColor2_rpg():
    name = "Robin"
    returnValueColor =  playersColor_rpg(name)
#   DARK_GREEN 0x1F8B4C
    assert(7419530 == returnValueColor )

#13 integration test big bang , Unit being used are Player, Item, and AllPlayersData
def test_fight_rpg():
#   create two chars one person has equiped items and the other does not but has something inventory
    player1 = Player("name1", 143225)
    player2 = Player("name2", 134336)
    
    player1.equipItem(Item("name", strength=5, defense=0, pg=0))
    player1.equipItem(Item("name", strength=5, defense=0, pg=0))
    player2.addItem((Item("name", strength=200, defense=0, pg=0)))
    
#   call fight_rpg should output 
    returnsWinnersID = fight_rpg(serverPlayers, player1, player2)
    
    assert(returnsWinnersID == 1)
    
#   test that we get the right player and that the player has the following items returnPlayer
#14 integration test big bang  Unit being used are Player, Item, and AllPlayersData
def test_that_returnPlayer():
#   make sure that items are all added to write place
    player1 = Player("Jeffrey", 43897)
    player1.addItem((Item("Nomy", strength=200, defense=0, pg=0)))# add to inventory
    player1.equipItem(Item("stick", strength=5, defense=0, pg=0))#  add to equipped
    serverPlayers.addplayertoList(player1)
    
    returnedPlayer = serverPlayers.returnPlayer(43897)    
    invenotryItem = returnedPlayer.inventory[0].name# from spot 0
    equippedItem = returnedPlayer.equipped[0].name# from spot 0 
    
#   call fight_rpg should output 
    
    assert(invenotryItem == "Nomy" and equippedItem == "stick")

# def playersColor_rpg(playerName):
#     letterQuan = 0#283
#     for i in range(len(playerName)):
#         letterQuan = letterQuan + ord(playerName[i])
#     trueColor = letterQuan % 6 
    
# #   options
# #   AQUA
#     if  trueColor == 0:
#         return 1752220
# #   DARK_GREEN	
#     if  trueColor == 1:
#         return 2067276
# #   DARK_PURPLE	
#     if  trueColor == 2:
#         return 7419530
# #   GOLD
#     if  trueColor == 3:
#         return 15844367
# #   RED
#     if  trueColor == 4:
#         return 15158332
# #   NAVY	
#     if  trueColor == 5:
#         return 15158332
# #   BLURPLe
#     if  trueColor == 6:
#         return 15158332

#   16 white box testing branching coverage
def test_Color():

    result1 = playersColor_rpg("B")
    result2 = playersColor_rpg("C")
    result3 = playersColor_rpg("D")
    result4 = playersColor_rpg("E")
    result5 = playersColor_rpg("F")
    result6 = playersColor_rpg("G")
    assert (result1 == 1752220)
    assert (result2 == 2067276)
    assert (result3 == 7419530)
    assert (result4 == 15844367)
    assert (result5 == 15158332)
    assert (result6 == 15158332)
    
    
    
    
