import json
import discord
import os
import basic.methods as bm
from discord.ui import Button, View    
from datetime import time

# constant to represent the max number of profiles
MAX_NUM_PROFILES = 100

# Event class will store all of the information regarding a particular event. 
class Event:
    start_time = time()
    end_time = time()
    def __init__(self, name, notes, starthour, endhour, startmin, endmin):
        self.name = name
        self.notes = notes
        self.start_time.hour = starthour
        self.start_time.minute = startmin
        self.start_time.hour = endhour
        self.start_time.min = endmin

# List profiles function. 
async def list_profiles(interaction: discord.Interaction):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # grabbing the path of the json file for this server

    listOfProfiles = []

    # Reading JSON file and storing it in listObj as a list of dictionaries, each dictionary is a profile
    with open(path) as fp:
        listOfProfiles= json.load(fp)
    
    if(len(listOfProfiles) == 0):
        await bm.send_msg(interaction, "No profiles have been created on this server!")
        return
    
    embed=discord.Embed(title="Profiles", description="All schedules in the server ", color=0x8208d4)
    embed.add_field(name="Page 1/20", value="", inline=False)
    embed.set_footer(text="Joe\nMuhamad\nJudah\nShawyan\nAlex")

    # function is called whenever the left arrow button is clicked
    async def left_arrow_callback(interaction):
        left_arrow.disabled = True
        await interaction.response.edit_message(view=view)
        await bm.follow_up(interaction, "Left arrow has been clicked")
    
    # function is called whenever the right arrow button is clicked
    async def right_arrow_callback(interaction):
        right_arrow.disabled = True
        await interaction.response.edit_message(view=view)
        await bm.follow_up(interaction, "Right arrow has been clicked!")
    
    # creating the buttons
    left_arrow = Button(label="🡠", style=discord.ButtonStyle.primary)
    left_arrow.callback = left_arrow_callback

    right_arrow = Button(label="🡢", style=discord.ButtonStyle.primary)
    right_arrow.callback = right_arrow_callback

    # Creating the view to display the buttons
    view = View()
    view.add_item(left_arrow)
    view.add_item(right_arrow)
    await interaction.response.send_message(embed=embed, view=view)

# Takes in profile name, profile notes, and the Interaction object. 
# The function returns either 0, 1, or 2. A 0 indicates a failure to create the profile for any reason, a 1 represents successful 
# creation of the profile, and a 2 represents that a profile with the same name already exists
async def add_profile(interaction: discord.Interaction, name: str, notes: str):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    
    listOfProfiles = []

    # Reading JSON file and storing it in listObj as a list of dictionaries, each dictionary is a profile
    with open(path) as fp:
        listOfProfiles= json.load(fp)

    # Checking if the profile exists, if not, continue as normal. If so, let the user know and leave the function
    if(profile_exists(interaction, name, listOfProfiles)):
        await bm.send_msg(interaction, "A profile with the same name already exists!")
        return    

    # Creating the profile as a dictionary, no events are on it by default
    profile = {"name":name, "notes":notes, "events":[]}
    
    listOfProfiles.append(profile)

    # dumping the profile contents in the JSON
    with open(path, "w") as f:
        json.dump(listOfProfiles, f, 
                  indent=2, 
                  separators=(",",": "))

    await bm.send_msg(interaction, "Profile Successfully Created")

async def delete_profile(interaction: discord.interaction, profile_name: str):
    return

async def add_event(interaction: discord.Interaction, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int):
    return

# Takes in the name of the profile and the interaction object, searches through JSON file and checks of a profile of the given name already exists
# returns a 0 if the profile doesn't exist, a 1 if it does
def profile_exists(interaction: discord.Interaction, name: str, listOfProfiles):
    # looping through the list of profiles, and checking each of the profile names to see if a profile exists with the same name as the given name
    for profile in listOfProfiles:
        if(profile["name"] == name):
            return 1
    return 0

# Takes in 3 integers as input
# makes sure that the number given as a parameter is less than or equal to the upper bound and greater than or equal to the lower bound
# returns 0 if the number is not within bounds, returns 1 if the number is within the bounds
def within_bounds(number: int, lowerBound: int, upperBound: int):
    if(number >= lowerBound and number <= upperBound):
        return 1
    else:
        return 0