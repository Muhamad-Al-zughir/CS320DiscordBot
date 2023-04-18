# shbang
# Started 1/18/2023

import os
import sys
import discord
from discord import app_commands
from dotenv import load_dotenv
import json

# Add your imports below here, if in a folder, use a dot instead of a slash
import botgame.game as botgame
import libgen.lib_handler as lb
import closedai.ai_handler as aih
import scheduler.schedule as schedule
import music.muzique as mzb
import mathcalc.math as calc

# setting up the needed intents
intents = discord.Intents.all()
intents.message_content = True          # setting message_content to True in order to read messages
client = discord.Client(intents=intents)

# tree which will hold all of the client commands
tree = app_commands.CommandTree(client)

load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('DISCORD_API')


# Openai variables
caiSettings = {
    'temp': 0.6,
    'results': 1,
    'maxTokens': 1000,
}
messages = [] # Array of the conversation with closedai

# Implement all the slash commands here, write down whos is which.
@tree.command(name = "libgen", description = "Search for books")
@app_commands.describe(type="Please enter either \"author\" or \"title\"", search="Search, must be at least 3 characters")
async def basic_libgen(interaction, type: str, search: str): # Set the arguments here to get options on the slash commands.
    await lb.handleLibSearch(interaction, type, search)

@tree.command(name = 'listmodels', description="List all models available by closedai")
async def list_models(interaction: discord.Interaction): # Set the arguments here to get options on the slash commands.
    # Get the list of models from the handler, which just formats the list of models into a nice string
    str = aih.getModels()
    cool_str = aih.codefiy(str)
    await interaction.response.send_message(cool_str)

@tree.command(name = 'listsettings', description='List the current settings for closedai')
async def list_settings(interaction: discord.Interaction):
    settings = caiSettings # Closed ai settings
    str = ''
    # Loop through the dictionary, creating a cool string
    for key in settings:
        newStr = f"{key}: {settings[key]}"
        str += f"\n{newStr}"
    cool_str = aih.codefiy(str)
    await interaction.response.send_message(cool_str)

# Change a setting
@tree.command(name='changesetting', description='Change a particular setting, related to the closed ai completion prompts')
@app_commands.describe(key="Should be one of the keys listed in \"listsettings\"", value="Depends on the setting, should be a number")
async def change_setting(interaction: discord.Interaction, key: str, value: str):
    # Gets the allowed keys from the dict
    allowed = list(caiSettings.keys())

    # Check if the key sent is one of the allowed
    if (key not in allowed):
        await interaction.response.send_message('Setting not found')
        return
    val = aih.convertToFloatOrInt(value)
    caiSettings[key] = val
    await interaction.response.send_message('Setting Changed.')

# List the commands available to closed ai, and what they do.
@tree.command(name='caioptions', description="List all of the functionalities related to the closed ai")
async def cai_options(interaction: discord.Interaction):
    await aih.sendCaiOptions(interaction)

# Completion call, takes in a prompt, and generates a response with it. NOTE: uses the caiSettings
@tree.command(name='caigpt', description="Takes in a prompt, returns a GPT-3.5 response, keeps track of conversation")
@app_commands.describe(prompt="Text prompt, can be anything, should not be empty")
async def cai_completion(interaction: discord.Interaction, prompt: str):
    # Immediately respond, (could just defer), as larger API calls can cause timeouts
    await interaction.response.send_message('Prompt Recieved, Loading...')
    item = aih.genConvoItem(prompt)
    messages.append(item)

    # Get a completion from the handler, hand it the messages array and the settings
    res = aih.getCompletion(messages, caiSettings)
    if not res:
        await interaction.followup.send('An error occured while creating a completion')
        return
    
    # Loop through the completions, add all the messages to the messages array
    for val in res['completions']:
        messages.append(val['message'])
    # The above allows for gpt to have access to the whole conversation, making it more chatlike.

    await aih.sendResponses(interaction, res, caiSettings)

# Image generation, uses openai's DALLE program, should be pretty neat
@tree.command(name='dalle', description="Generates images based on a given prompt, using closedais DALL-E")
@app_commands.describe(prompt="Text prompt, should describe the desired image", results="Number of results, should be between 1-10")
async def dalle_gen(interaction: discord.Interaction, prompt: str, results: int):
    # Verify the integer given is between 1 & 10
    if (results < 1 or results > 10):
        await interaction.response.send_message('Result param must be between 1-10')
        return

    # Send a message anyway (could defer) to stop timeouts
    await interaction.response.send_message('Recieved Prompt, Loading...')
    # Hand prompt and desired result amount to the genImages function
    urls = aih.genImages(prompt, results)
    if not urls:
        await interaction.followup.send('An error occured while generating images')
        return
    embeds = []
    # Loop through the urls, and send them all to discord
    for url in urls:
        embed=discord.Embed(title='DALLE generated image')
        embed.set_image(url=url)
        embeds.append(embed)
    str = f"Generated {len(urls)} image(s) from the prompt: *{prompt}*"
    # Send all the images at once.
    await interaction.followup.send(content=str, embeds=embeds)
 #  ==================================================

# spidergif command: After the running of the command the bot will respond by posting a funny spider gif
@tree.command(name = 'spidergif', description = 'Bot will post a funny spider gif')
async def spider_gif(interaction: discord.Interaction):
    await interaction.response.send_message('https://media.discordapp.net/attachments/721098895152775288/1001770030352060456/image0.gif')
 #  ==================================================

# listProfiles command: After the running of the command the bot will post all the profiles that have been created 10 profiles at a time. Users will be able to use buttons to view the other profiles if there are more than 10
@tree.command(name = 'listprofiles', description = 'Bot will list out all the profiles created on this server')
async def list_profiles_cmd(interaction: discord.Interaction):
    # responding by printing out the profiles using discord embed features
    await schedule.list_profiles(interaction)
 #  ==================================================

# viewprofile command: After the running of the command the bot will list out all of the events of a given profile with the list of events for each given day of the week. 
@tree.command(name = 'viewprofile', description = 'Bot will list out all the profiles created on this server')
@app_commands.describe(name="Name of the profile to be viewed (PROFILE MUST EXIST)")
async def view_profile_cmd(interaction: discord.Interaction, name: str): 
    # responding by printing out the profiles using discord embed features
    await schedule.view_profile(interaction, name)
 #  ==================================================

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'addprofile', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(name="Name of the profile to be created (NAME MUST NOT ALREADY BE IN USE)", notes="Any important notes regarding the profile")
async def add_profile_cmd(interaction: discord.Interaction, name: str, notes: str):
    await schedule.add_profile(interaction, client, name, notes)

# deleteprofile command: Takes in profile name. After running the command the bot will delete the profile with the given name
# Name of the profile must be of an existing profile
@tree.command(name = 'deleteprofile', description = 'Bot will delete a profile with the given name')
@app_commands.describe(name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)")
async def delete_profile_cmd(interaction: discord.Interaction, name: str):
    await schedule.delete_profile(interaction, name)
 #  ==================================================

# addevent command: 
@tree.command(name = 'addevent', description = 'Bot will add a profile with the given name and notes')
@app_commands.describe(profile_name="Name of the profile for which the event should be added to", event_name="Name of the event to be added",
                        event_notes="Notes regarding the event", start_hour="The hour the event starts (must be integer between 0 and 23 inclusive)",
                        start_min="minute the event starts", end_hour="The hour the event ends at (must be integer between 0 and 23 inclusive)",
                        end_min="The minute which the event ends at", day="Enter a number 1-7 to represent the day of the week (1=Sun, 2=Mon, 3=Tue, 4=Wed, 5=Thu, 6=Fri, 7=saturday)")
async def add_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int, day: int):
    await schedule.add_event(interaction, client, profile_name, event_name, event_notes, start_hour, start_min, end_hour, end_min, day)
 #  ==================================================

# addprofile command: Takes in profile name and profile notes after running the command the bot will create a profile with the given attributes. 
# Name of the profile must not already be in use though. 
@tree.command(name = 'deleteevent', description = 'Bot will delete a event with the given name')
@app_commands.describe(profile_name="Name of the profile to be deleted(PROFILE MUST ALREADY EXIST)",
                       event_name="Name of event to be deleted (EVENT MUST ALREADY EXIST)")
async def delete_event_cmd(interaction: discord.Interaction, profile_name: str, event_name: str):
    await schedule.delete_event(interaction, client, profile_name, event_name)
 #  ==================================================

# googlecalendar
@tree.command(name = 'googlecalendar', description = 'Takes the given profile name and creates a visual weekly schedule using google calendar')
@app_commands.describe(profile_name="Name of the profile to be used")
async def google_calendar_cmd(interaction: discord.Interaction, profile_name: str):
    await interaction.response.defer()
    await schedule.google_calendar(interaction, profile_name)
    os.remove("myscreenshot.png")
    os.remove("mycroppedscreenshot.png")

# viewprofile command: After the running of the command the bot will list out all of the events of a given profile with the list of events for each given day of the week. 
@tree.command(name = 'helpscheduler', description = 'Bot will bring forth a help page detailing all of the commands and how to use them')
async def help_scheduler_cmd(interaction: discord.Interaction): 
    # responding by printing out the profiles using discord embed features
    await schedule.help_scheduler(interaction)

# Bot will join Discord Voice channel
@tree.command(name = 'move', description = 'Bot will join your voice channel')
async def move(interaction: discord.Interaction):     
    await mzb.move(interaction)
 #  ==================================================

# Streams from a YouTube, SoundCloud, or Spotify Link
@tree.command(name = 'play', description = 'Enter a valid YouTube, SoundCloud, or Spotify Link')
async def play(interaction: discord.Interaction, url:str):
    await mzb.play(interaction,url,client)
 #  ==================================================
    
# End Stream
@tree.command(name = 'clear', description = 'Bot will clear all playing music')
async def clear(interaction: discord.Interaction):
    await mzb.clear(interaction)
 #  ==================================================

# Pause Stream and Unpause Stream
@tree.command(name = 'pause-unpause', description = 'Bot will pause the currently playing song or unpause if one was being played')
async def pause_yt(interaction: discord.Interaction):
    await mzb.pause_yt(interaction)
 #  ==================================================

# Skip currently playing song
@tree.command(name = 'skip', description = 'Bot will skip the currently playing song')
async def skipSong(interaction: discord.Interaction):
    await mzb.skipSong(interaction, client)
 #  ==================================================

# Display current queue 
@tree.command(name = 'queue', description = 'Display the current active music queue')
async def displayQueue(interaction: discord.Interaction):
    await mzb.displayQueue(interaction, client)
 #  ==================================================

# Shuffle Current Queue
@tree.command(name = 'shuffle', description = 'Shuffle and display current active music queue')
async def shuffleQueue(interaction: discord.Interaction):
    await mzb.shuffleQueue(interaction, client)
 #  ==================================================

# Shift song for a certan value in seconds 
@tree.command(name = 'shiftsong', description = 'Shift a song forward or backward for a valid number of seconds')
async def fastForwardSong(interaction: discord.Interaction, seconds: int):
    await mzb.fastForwardSong(interaction, client, seconds)
 #  ==================================================

# Repeat a song
@tree.command(name = 'encore', description = 'Repeat the currently playing song')
async def encore(interaction: discord.Interaction):
    await mzb.encore(interaction,client)    
 #  ==================================================

# Swap Two Indexes for a Song queue
@tree.command(name = 'swap', description = 'Swap two indexes of a queue')
async def swap(interaction: discord.Interaction, indexone: int, indextwo: int):
    await mzb.swap(interaction,client,indexone,indextwo)
 #  ==================================================

# Display Song Informatiom
@tree.command(name = 'displayinfo', description = 'Display information about the current song / video')
async def swap(interaction: discord.Interaction):
    await mzb.displayInfo(interaction,client)
 #  ==================================================

# Display Song Lyrics
@tree.command(name = 'displaylyrics', description = 'Display Lyrics for the current playing song')
async def displayLyrics(interaction: discord.Interaction):
    await mzb.displayLyrics(interaction,client)
 #  ==================================================

# Shift song for a certain percentage value of total runtime
@tree.command(name = 'shiftsong_percent', description = 'Shift to a certain percentage of the total runtime of the current track')
async def percentageShift(interaction: discord.Interaction, percent: int):
    await mzb.percentageShift(interaction, client, percent)
 #  ==================================================

# Add a playlist IF a song is already playing
@tree.command(name = 'addplaylist', description = 'add a youtube playlist to queue')
async def addPlaylist(interaction: discord.Interaction, url: str):
    await mzb.addPlaylist(interaction, client, url)
#  ==================================================

# Display information about an Album using the Wikipedia and Spotify APIs
@tree.command(name = 'aboutthealbum', description = 'display info about a song album')
async def aboutTheAlbum(interaction: discord.Interaction):
    await mzb.aboutTheAlbum(interaction,client)
 #  ==================================================

# Display Information about an Artist using the Wikipedia and Spotify APIs
@tree.command(name = 'abouttheartist', description = 'display info about a song artist')
async def aboutTheAlbum(interaction: discord.Interaction):
    await mzb.aboutTheArtist(interaction,client)
 #  ==================================================

# Display Information about a song using the Wikipedia and Spotify APIs
@tree.command(name = 'aboutthesong', description = 'display info about a song')
async def aboutTheSong(interaction: discord.Interaction):
    await mzb.aboutTheSong(interaction,client)
 #  ==================================================

 # Music Help Command Function
@tree.command(name = 'musichelp', description = 'display information on commands')
async def musichelp(interaction: discord.Interaction):
    await mzb.musichelp(interaction)
#  ==================================================

 # Add Next function for muisc
@tree.command(name = 'addnext', description = 'add a song to the front of the queue')
async def addnext(interaction: discord.Interaction, url:str):
    await mzb.addNext(interaction, client, url)
#  ==================================================


#   dropdown menu for character selection
@tree.command(name = "rp_store", description = "store for rp game")
async def rp_store(interaction: discord.Interaction):
    await botgame.rp_store_gen(interaction)
 #  =======================================

#   dropdown menu for character selection
@tree.command(name = "rp_menu", description = "menu options for rp game")
async def rp_dropdown_menu_cmd(interaction: discord.Interaction):
    await botgame.rp_dropdown_menu(interaction)
 #  ===========================================
 
 #   create rp for character game
@tree.command(name = "create_rp_character", description = "character creation for game")
async def rp_character_create_cmd(interaction: discord.Interaction):
    await botgame.rp_character_create(interaction)
 #  ==================================================

 #   create rp for character game
@tree.command(name = "rp_challenge", description = "able to challenge a member  in rp game")
async def rp_challenge_calling(interaction: discord.Interaction):
    await botgame.rp_challenge(interaction)
 #  ===================================================

 #  update roles
@tree.command(name = "rp_update_roles", description = "updates everyones roles in server")
async def rp_update_roles(interaction: discord.Interaction):
    await botgame.rp_update_roles_function(interaction,client)
 #  =========================================================

 #  update roles
@tree.command(name = "rp_schedule", description = "checks up on everyone")
async def rp_schedule(interaction: discord.Interaction):
    await botgame.clearDaily_rpg(interaction, client)
 #  ================================================
 
 #  update roles
@tree.command(name = "rp_fight", description = "enter opponents id to fight")
@app_commands.describe(opp="Please enter opponents ID" )
async def rp_slash_fight(interaction: discord.Interaction, opp: str):
    await botgame.rp_fight_wrapper(interaction, client, opp)
 #  ===================================================
 
#   Shut down Bot safely
@tree.command(name = "shutdown", description = "shuts down the bot SAFELY")
async def shutdown(interaction: discord.Interaction):
    await interaction.response.send_message(f'Shutting down bot. Goodbye!')
    await client.close()
#   ===================================================

 
#This command does the simple description of the math commands
@tree.command(name = "simplemathhelp", description="Simplified version of instructions")
async def simplemathhelp(interaction: discord.Interaction):
    await interaction.response.send_message(calc.simplehelp())


#This convert from one temperature to another : K, F, C
@tree.command(name = "tempconversion", description="Convert between Kelvin, Celsius, and Fahrenheit")
@app_commands.describe(temperature = "Enter the temperture.", current = "Select K, C, F to specify current", convert = "Select K, C, F to what to convert")
async def tempconversion(interaction: discord.Interaction, temperature: float, current: str, convert: str):
    if current != 'K' and current != 'C' and current != 'F':
        await interaction.response.send_message("The specified symbol under current variable is undentified.")
    if convert != 'K' and convert != 'C' and convert != 'F':
        await interaction.response.send_message("The specified symbol under convert variable is undentified")
    if (convert == current) or (current == convert) or (current == convert):
        await interaction.response.send_message("You have selected the same exact conversion.")
    await interaction.response.send_message(str(temperature) + ' ' + current + " is equal to " + str(calc.temperature(temperature, current, convert)) + " " + convert)


#Calls the simple integration functions
@tree.command(name = "integrate", description="This function performs basic integration")
@app_commands.describe(equation = "The equation that will be operated", low = "The lower bound, leave 'x' if not using", high = "The high bound, leave 'x' if not using")
async def integrate(interaction: discord.Interaction, equation: str, low: str, high: str):
    #print(low, high)
    equation = calc.tupleList(equation.split(" "))
    if (low == 'x' and high != 'x') or (low != 'x' and high == 'x'):
        await interaction.response.send_message("The bounds are not correct.")
    
    await interaction.response.send_message("The result for the integration is " + calc.integrate(equation, low, high))
  
  
#Calls the simple differentiation functions    
@tree.command(name = "differentiate", description="Enter a equation to differentiate on 'x'")
@app_commands.describe(equation = "The equation that you want to differentiate")
async def differentiate(interaction: discord.Interaction, equation: str):
    equation = calc.tupleList(equation.split(" "))
    await interaction.response.send_message("After differentiation : " + calc.differentiate(equation))


# This command is for the pythagorean theorem operations
#Can check whether valid right triangle and calculate missing sides
@tree.command(name = "pythagorean", description = "This function performs the Pythagorean Theorem. Mark 'x' for the side that is not known.")
@app_commands.describe(a = "One of the side lengths", b = "Another side length", c = "Hypotenuse")
async def pythagorean(interaction: discord.Interaction, a: str, b: str, c: str):
    if a == "x":
        await interaction.response.send_message("The 'a' side is " + str(calc.pythagoreanSide(b, c)))
    elif b == "x":
        await interaction.response.send_message("The 'b' side is " + str(calc.pythagoreanSide(a, c)))
    elif c == "x":
        await interaction.response.send_message("The 'c' side (hypotenuse) is " + str(calc.pythagoreanHypotenuse(a, b)))
    else:
        await interaction.response.send_message(calc.pythagoreanCheck(a, b, c))


#More detailed description of the math commands
@tree.command(name = "mathhelp", description= "Help message how to use the math funcitons")
@app_commands.describe(number = "Enter 1 or 2 to see the pages to see how to use the math funcitons.")
async def mathhelp(interaction: discord.Interaction, number: str):
    if number == '1':
        message = calc.message1()
    elif number == '2':
        message = calc.message2()
    else:
        await interaction.response.send_message("Try again.")
    
    await interaction.response.send_message(message)


#Does the rectangle operations and calls their functions
@tree.command(name = "rectangle", description="Use to calculate area or perimeter of a rectangle")
@app_commands.describe(side1 = "Enter one of the sides", side2 = "Enter another side", operation="Enter : 'perimeter' or 'area'")
async def circle(interaction: discord.Interaction, side1: str, side2: str, operation: str):
    if operation == "area":
        await interaction.response.send_message("Area : " + str(calc.areaRectangle(side1, side2)))
    elif operation == "perimeter":
        await interaction.response.send_message("Perimeter : " + str(calc.perimeterRectangle(side1, side2)))
    else:
        await interaction.response.send_message("Operation entered does not exist.\nTry again.")


#Does the circle operations and calls their functions
@tree.command(name = "circle", description="Use to calculate area or circumfrance of a circle")
@app_commands.describe(radius = "Enter the redius length", operation="Enter : 'circumference' or 'area'")
async def circle(interaction: discord.Interaction, radius: str, operation: str):
    if operation == "area":
        await interaction.response.send_message("Area : " + str(calc.areaCircle(radius)))
    elif operation == "circumference":
        await interaction.response.send_message("Circumfrance : " + str(calc.circumferenceCircle(radius)))
    else:
        await interaction.response.send_message("Operation entered does not exist.\nTry again.")


#Does the other triangle operations, area.
@tree.command(name = "triangle", description="Use to calculate area of a triangle")
@app_commands.describe(base = "Enter the base length", height = "Enter the height length", operation = "Enter : 'area'")
async def triangle(interaction: discord.Interaction, base: str, height: str, operation: str):
    if operation == "area":
        await interaction.response.send_message("Area : " + str(calc.areaTriangle(base, height)))
    else:
        await interaction.response.send_message("Operation entered does not exist.\nTry again.")


# This command give the options for the user to work with two fractions,
# They can get the GCD, LCD from the fractions, as well as multiply, divide, subtract and add
# and return the result in simplified form
@tree.command(name = "fraction", description = "Fraction operations")
@app_commands.describe(fraction1 = "Please enter the two fractions that you want to work with. Ex: 1/2", operation = "Enter one of the following : LCD, GCD, Add, Subtract, Multiply, Divide")
async def fraction(interaction: discord.Interaction, fraction1: str, fraction2: str, operation: str):
    if operation == "LCD":
        await interaction.response.send_message("LCD : " + str(calc.lcd(fraction1, fraction2)))
    elif operation == "GCD":
        await interaction.response.send_message("GCD : " + str(calc.gcd(fraction1, fraction2)))
    elif operation == "Add":
        await interaction.response.send_message("Final fraction : " + calc.addFraction(fraction1, fraction2))
    elif operation == "Subtract":
        await interaction.response.send_message("Final fraction : " + calc.subtractFraction(fraction1, fraction2))
    elif operation == "Multiply":
        await interaction.response.send_message("Final fraction : " + calc.multiplyFraction(fraction1, fraction2))
    elif operation == "Divide":
        await interaction.response.send_message("Final fraction : " + calc.divideFraction(fraction1, fraction2))
    else:
        await interaction.response.send_message("Operation that was entered is not recognized. Try again.")


#takes in two polynomials, each having two variable. and returns the calculated values of the variables that will make the equations equal
@tree.command(name = "polynomialtwo", description="Enter two equations with each having two variables: x and y")
@app_commands.describe(equation1 = "Enter the first equation", equation2 = "Enter in the second equation")
async def polynomialtwo(interaction: discord.Interaction, equation1: str, equation2: str):
    equation1 = calc.tupleList(equation1.split(" "))
    equation2 = calc.tupleList(equation2.split(" "))
    (x, y) = calc.polynomialTwo(equation1, equation2)
    if x == 0 and y == 0:
        await interaction.response.send_message("Please try another pair of equations")
    await interaction.response.send_message("X = " + str(x) + "\nY = " + str(y))


 # calculate simple equation using proper order of operations
@tree.command(name = "equation", description = "Simple equation")
@app_commands.describe(simple = "Please enter a simple equation with each spaces in between")
async def equation(interaction: discord.Interaction, simple: str):
    equation = list(simple.split(" "))
    print(equation)
    if (reason := calc.simpleCheck(equation)) != True:
        print(reason)
        await interaction.response.send_message("The equation sent in not a valid simple equation. Try again.\nReason: " + reason)
    #result = checker(equation)
    else:
        await interaction.response.send_message(calc.checker(equation))
       
        
 # calculate algebra equation, needs specification of what to do
 #slope - slope- intercept form
 #simplify - simplifies the algebra equation to its simplest form
 #quadratic - finds the x - intercepts using teh quadratic formula
@tree.command(name = "algebra", description = "Algebra calculator with several options")
@app_commands.describe(equation = "Please enter an algebra equation with spaces in between", answer = "Enter the following: (slope) - slope intercept form, (simplify) - simplify the equation, (quadratic) - quadratic formula")
async def algebra(interaction: discord.Interaction, equation: str, answer: str):
    equation = list(equation.split(" "))
    if answer == "slope":
        result = (calc.slope(equation, answer))
        slope = result[0]
        intercept = result[1]
        await interaction.response.send_message("The slope of the equation is " + str(slope) + ".\nThe y-intercept of the equation is " + str(intercept))
    elif answer == "simplify":
        result = calc.tupleList(equation)
        print(result)
        result = calc.algebraSimplify(result)
        print(result)
        await interaction.response.send_message("The simplify equation is " + result)
    elif answer == "quadratic":
        print(equation)
        result = calc.tupleList(equation)
        print(result)
        (x1, x2) = calc.quadratic(result)
        await interaction.response.send_message("The x-intercepts are : " + str(x1) + " and " + str(x2))


# client event to take place whenever the client joins a server.
# it will create a new json file in the scheduler directory to store the data associated with this newly joined guild
@client.event
async def on_guild_join(guild):
    path = "scheduler/" + str(guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory 
    try:
        file = open(path, "x")
        # initializing the json file with a list in order that we make easy appends to it
        listObj = []
        json.dump(listObj, file)
        print("Making file" + path)
        file.close()
    # if the file exists
    except FileExistsError:
        print("File exists " + path)
 #  ==================================================

#   give gold
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author != client.user:
        await botgame.rp_message_goldf(message)
 #  ==================================================

# Begin Bot
@client.event
async def on_ready():
    await tree.sync()
    print(f'{client.user} has connected to Discord!')
 #  ==================================================

 # Send Standard Error to Discord Channel
async def errorLogs(message):
    channel = await client.fetch_channel(1094498464710262865)                   # Discord Channel Specified Here

    spam = ['rate limited', 'logging in', 'connected to Gateway',               # spam and incorrectly labeled "error messages" in stderr
            'handshake complete','Starting voice','voice...'
            'ffmpeg process', 'should have terminated', 'has not terminated']     

    if any(substring in message for substring in spam ):                        # Ignore Spam
        return


    if len(str(message)) < 1900:                                                # Due to discord limitations, need to print description 1900 at a time
        await channel.send(f"**STDERR Output:**\n```\n{str(message)}\n```")     # If less than 1900, send immediately
    else:
        await channel.send(f'**STDERR Output:**\n')
        newerr = ''                                                             # Else, declare new variable to track 1900 chars at a time
        while len(message) > 1900:                                              # Iterate 1900 at a time while output is greather than 1900
                    
            newerr = message[:1900]                                             # string slicing to grab 1900 and send
            await channel.send(f"```\n{str(newerr)}\n```")
            message = message[1900:]                                            # Error Updated Here                                     **    

        await channel.send(f"\n```\n{str(message)}\n```")

def errhandle(message):
     # Call the async function to send the error message to the Discord channel
     client.loop.create_task(errorLogs(message))
    
sys.stderr.write = errhandle                                                    # Standard Error redirection initialized here

client.run(TOKEN)
