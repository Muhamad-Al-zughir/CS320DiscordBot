import json
import discord
import math
import basic.methods as bm
from discord.ui import Button, View  
from time import sleep 
from datetime import time
import os
import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

# constants to represent the max number of profiles and events allowed (this is done to mimic a real product where too much data being used per server may be too expensive to have hosted if thousands of servers are using the bot)
MAX_NUM_PROFILES = 100
MAX_NUM_EVENTS = 40

# Profile class will store all the information regarding a particular class
class Profile:
    def __init__(self, name, notes, events):
        self.name = name
        self.notes = notes
        self.events = events

# Event class will store all of the information regarding a particular event. 
class Event:
    def __init__(self, name, notes, starthour, endhour, startmin, endmin, day):
        self.name = name
        self.notes = notes
        self.start_hour= starthour
        self.start_min = startmin
        self.end_hour = endhour
        self.end_min = endmin
        self.day = day

# List profiles function. 
async def list_profiles(interaction: discord.Interaction):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)
    
    # Checking to make sure that there are indeed profiles on the server that have been created. 
    if(len(list_of_profiles) == 0):
        await bm.send_msg(interaction, "No profiles have been created on this server!")
        return
    
    # Finding the number of pages that will be needed to display all the profiles
    # (10 profiles displayed per page)
    num_pages = math.ceil(len(list_of_profiles)/10) # total number of pages needed
    curr_page = 1   # Variable to keep track of which page you are on

    # Generating the footer text by grabbing the names of the profiles. If there are more than 10 profiles then we will grab only the first 10 names and leave out the rest
    footer_text = ""
    profile_ind = 0
    
    # Grabbing the footer text by looping through the list of profiles and grabbing the names and concatenating footer text with it
    # The [0:] just means start at index 0
    for profile in list_of_profiles[0:]:
        footer_text = footer_text + profile["name"] + "\n"
        profile_ind = profile_ind + 1
        if(profile_ind%10 == 0):
            break
    profile_ind = 0

    # Creating the embed to be displayed
    embed=discord.Embed(title="Profiles", description="All schedules in the server ", color=0x8208d4)
    embed.add_field(name=f"Page {curr_page}/{num_pages}", value="", inline=False)
    embed.set_footer(text=footer_text)

    # function is called whenever the left arrow button is clicked
    async def left_arrow_callback(interaction):
        nonlocal curr_page 
        nonlocal profile_ind
        curr_page = curr_page - 1

        # if this is the first page, disable the arrow
        if(curr_page == 1):
            left_arrow.disabled = True

        # The fact that we were able to click on the left arrow in the first place suggests that there are pages that can be accessed by the right arrow button
        if(right_arrow.disabled == True):
            right_arrow.disabled = False
        
        ############## Changing the embed ###############
        footer_text = ""

        # Setting the profile index to how it should be in the previous page
        profile_ind = profile_ind - 10

        # The [profile_ind:] just means start at the index of profile_ind
        for profile in list_of_profiles[profile_ind:]:
            footer_text = footer_text + profile["name"] + "\n"
            profile_ind = profile_ind + 1
            if(profile_ind%10 == 0):
                break
        if(profile_ind%10 == 0):
            profile_ind = profile_ind - 10
        else:
            profile_ind = profile_ind - (profile_ind%10)

        # Creating the embed to be displayed
        embed=discord.Embed(title="Profiles", description="All schedules in the server ", color=0x8208d4)
        embed.add_field(name=f"Page {curr_page}/{num_pages}", value="", inline=False)
        embed.set_footer(text=footer_text)
        #################################################

        await interaction.response.edit_message(embed=embed, view=view)
    
    # function is called whenever the right arrow button is clicked
    async def right_arrow_callback(interaction):
        nonlocal curr_page 
        nonlocal profile_ind

        curr_page = curr_page + 1   # Incrementing the current page

        # If this is the last page, disable the right arrow button
        if(curr_page == num_pages):
            right_arrow.disabled = True
        
        # The fact that we were able to click on the right arrow in the first place suggests that there are pages that can be accessed by the left arrow button
        if(left_arrow.disabled == True):
            left_arrow.disabled = False

        ############## Changing the embed ###############
        footer_text = ""

        profile_ind = profile_ind + 10

        # Grabbing the footer text
        # The [ind:] just means start at index 0
        for profile in list_of_profiles[profile_ind:]:
            footer_text = footer_text + profile["name"] + "\n"
            profile_ind = profile_ind + 1
            if(profile_ind%10 == 0):
                break
        if(profile_ind%10 == 0):
            profile_ind = profile_ind-10
        else:
            profile_ind = profile_ind - (profile_ind%10)

        # Creating the embed to be displayed
        embed=discord.Embed(title="Profiles", description="All schedules in the server ", color=0x8208d4)
        embed.add_field(name=f"Page {curr_page}/{num_pages}", value="", inline=False)
        embed.set_footer(text=footer_text)
        #################################################

        await interaction.response.edit_message(embed=embed, view=view)
    
    # creating the buttons
    left_arrow = Button(label="🡠", style=discord.ButtonStyle.primary, disabled=True)
    left_arrow.callback = left_arrow_callback


    right_arrow = Button(label="🡢", style=discord.ButtonStyle.primary)

    # if there is only one page, we disable the right arrow button
    if(curr_page == num_pages):
        right_arrow.disabled = True

    right_arrow.callback = right_arrow_callback

    # Creating the view to display the buttons
    view = View()
    view.add_item(left_arrow)
    view.add_item(right_arrow)
    await interaction.response.send_message(embed=embed, view=view)

# view_profile will list out the events of a profile in a formatted manner through the use of discord buttons
# function takes in the discord interaction object and the name of the profile. 
# Note that the function will default to displaying Sunday as the default and initial day of the week for which events would be displayed
async def view_profile(interaction: discord.Interaction, profile_name: str):
    day_of_week = 1 # day of week is initally set to sunday (1 = sunday, 7 = saturday)
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists, if not, continue as normal. If so, let the user know and leave the function
    if(profile_exists(profile_name, list_of_profiles) == 0):
        await bm.send_msg(interaction, "Profile does not exist!")
        return
    
    selectedProfile = {}
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            selectedProfile = profile
    
    # Grabbing the footer text
    footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
    # Grabbing the number of events on a specific day
    num_events = num_events_on_day(selectedProfile["events"], day_of_week)
    # Creating the embed to be displayed
    embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)
    
    async def sunday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        sunday_btn.disabled = True
        day_of_week = 1

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def monday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        monday_btn.disabled = True
        day_of_week = 2

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def tuesday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        tuesday_btn.disabled = True
        day_of_week = 3

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def wednesday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        wednesday_btn.disabled = True
        day_of_week = 4

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def thursday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        thursday_btn.disabled = True
        day_of_week = 5

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def friday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        friday_btn.disabled = True
        day_of_week = 6
    
        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)

    async def saturday_callback(interaction):
        nonlocal day_of_week
        disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn)
        saturday_btn.disabled = True
        day_of_week = 7

        # Grabbing the footer text
        footer_text = grab_text_events_day(selectedProfile["events"], day_of_week)
        # Grabbing the number of events on a specific day
        num_events = num_events_on_day(selectedProfile["events"], day_of_week)
        # Creating the embed to be displayed
        embed = return_embed_view_profile(profile_name, num_events, day_of_week, footer_text)

        await interaction.response.edit_message(embed=embed, view=view)
    
    # Creating the buttons
    sunday_btn = Button(label="Sunday", style=discord.ButtonStyle.primary, disabled=True)   # Sunday button is initally disabled because 
    sunday_btn.callback = sunday_callback

    monday_btn = Button(label="Monday", style=discord.ButtonStyle.primary)
    monday_btn.callback = monday_callback

    tuesday_btn = Button(label="Tuesday", style=discord.ButtonStyle.primary)
    tuesday_btn.callback = tuesday_callback

    wednesday_btn = Button(label="Wednesday", style=discord.ButtonStyle.primary)
    wednesday_btn.callback = wednesday_callback

    thursday_btn = Button(label="Thursday", style=discord.ButtonStyle.primary)
    thursday_btn.callback = thursday_callback

    friday_btn = Button(label="Friday", style=discord.ButtonStyle.primary)
    friday_btn.callback = friday_callback

    saturday_btn = Button(label="Saturday", style=discord.ButtonStyle.primary)
    saturday_btn.callback = saturday_callback

    # Creating the view to display the buttons
    view = View()
    view.add_item(sunday_btn)
    view.add_item(monday_btn)
    view.add_item(tuesday_btn)
    view.add_item(wednesday_btn)
    view.add_item(thursday_btn)
    view.add_item(friday_btn)
    view.add_item(saturday_btn)
    await interaction.response.send_message(embed=embed, view=view)

    return

# Takes in profile name, profile notes, and the Interaction object. 
# The function returns either 0, 1, or 2. A 0 indicates a failure to create the profile for any reason, a 1 represents successful 
# creation of the profile, and a 2 represents that a profile with the same name already exists
async def add_profile(interaction: discord.Interaction, name: str, notes: str):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists, if not, continue as normal. If so, let the user know and leave the function
    if(profile_exists(name, list_of_profiles)):
        await bm.send_msg(interaction, "A profile with the same name already exists!")
        return    

    # Making sure the users do not exceed the maximum number of profiles allowed on a server
    if(len(list_of_profiles) >= MAX_NUM_PROFILES):
        await bm.send_msg(interaction, f"The max profile limit of {MAX_NUM_PROFILES} has been reached! Please delete some profiles to be able to create a new one.")
        return

    # Creating profile, then appending it as a dictionary
    profile = Profile(name, notes, [])
    list_of_profiles.append(profile.__dict__)

    # Sorting the list of events based on starting hour and starting minute (hour is of course of a higher priority than minute)
    list_of_profiles.sort(key = lambda x:x["name"])

    dump_list_of_profiles(path, list_of_profiles)

    await bm.send_msg(interaction, "Profile Successfully Created")

async def delete_profile(interaction: discord.Interaction, profile_name: str):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists
    if(profile_exists(profile_name, list_of_profiles) == 0):
        await bm.send_msg(interaction, "The profile you want to access does not exist!")
        return
    
    list_of_profiles = delete_profile_from_list(list_of_profiles)
            
    dump_list_of_profiles(path, list_of_profiles)
    
    await bm.send_msg(interaction, "Profile successfully deleted!")
    return

async def add_event(interaction: discord.Interaction, client: discord.Client, profile_name: str, event_name: str, event_notes: str, start_hour: int, start_min: int, end_hour: int, end_min: int, day: int):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists
    if(profile_exists(profile_name, list_of_profiles) == 0):
        await bm.send_msg(interaction, "The profile you want to access does not exist!")
        return
    
    is_valid_event = valid_event(start_hour, start_min, end_hour, end_min, day)

    if(is_valid_event != 1):
        await bm.send_msg(interaction, is_valid_event)
        return
    
    newEvent = Event(event_name, event_notes, start_hour, end_hour, start_min, end_min, day)

    # Creating the embed to be displayed
    embed=discord.Embed(title=f"Event to be created (reply 1 to confirm, anything else to cancel)", description=f"", color=0x8208d4)
    embed.add_field(name=f"Name: {event_name}\nNotes: {event_notes}\nTime: {start_hour}:{str(start_min).zfill(2)}-{end_hour}:{str(end_min).zfill(2)}", value="", inline=False)

    await interaction.response.send_message(embed=embed)

     # Grabbing the users response 
    # function to check if the user responding is the same person who made the command and is responding from the same channel
    def check(m):
        return m.channel == interaction.channel and m.author == interaction.user
    
    reply = await client.wait_for("message", check=check)
    # Parsing the input
    try:
        num_reply = int(reply.content)
        if (num_reply != 1): raise ValueError("outside bounds")
    except ValueError:
        await bm.follow_up(interaction, f"Ok! Event creation has been cancelled!") # Need to use a follow up after initial sending
        return

    if(num_reply == 1):
        for profile in list_of_profiles:
            if(profile["name"] == profile_name):
                if(len(profile["events"]) >= MAX_NUM_EVENTS):
                    await bm.send_msg(interaction, "Max event count reached for this profile")
                    return
                
                # Adding the event to the list in the form of a dictionary
                profile["events"].append(newEvent.__dict__)
                
                # Sorting the list of events based on starting hour and starting minute (hour is of course of a higher priority than minute)
                profile["events"].sort(key = lambda x:x["start_min"])
                profile["events"].sort(key = lambda x:x["start_hour"])
                profile["events"].sort(key = lambda x:x["day"])

                dump_list_of_profiles(path, list_of_profiles)

    await bm.follow_up(interaction, "New event successfully added!")
    

async def delete_event(interaction: discord.Interaction, client, profile_name: str, event_name:str):
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists
    if(profile_exists(profile_name, list_of_profiles) == 0):
        await bm.send_msg(interaction, "The profile you want to access does not exist!")
        return
    
    # Checking if an event with the given name existsexists
    if(event_exists(profile_name, event_name, list_of_profiles) == 0):
        await bm.send_msg(interaction, "The event you want to access does not exist!")
        return

    # Grabbing all the events with the same name as the given name and the number of those events
    numEvents = 0
    eventsWithSameName = []
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            for event in profile["events"]:
                if(event["name"] == event_name):
                    eventsWithSameName.append(event)
                    numEvents = numEvents + 1

    # Creating the footer text to be displayed on the embed by looping through the eventsWithSameName list, and adding the text of each event
    inc = 1     # incrementer to keep track of which number of profile we are on
    footer_text = ""
    for event in eventsWithSameName:
        note = event["notes"]
        start_hour = event["start_hour"]
        start_min = str(event["start_min"]) # setting the start_min as a string in order to utilize zfill method
        start_min = start_min.zfill(2)  # adding zeroes in front of the number until it's 2 digits long. For example, 1 becomes 01
        end_hour = event["end_hour"]
        end_min = str(event["end_min"]) # setting the end_min as a string in order to utilize zfill method
        end_min = end_min.zfill(2)    # adding zeroes in front of the number until it's 2 digits long. For example, 1 becomes 01
        day_of_week = ret_day_of_week(event["day"])

        footer_text = footer_text + f"({inc})\nNotes: {note}\nTime: {start_hour}:{start_min}-{end_hour}:{end_min}\nDay: {day_of_week}\n\n" 
        inc = inc+1

    # Creating the embed to be displayed
    embed=discord.Embed(title=f"Found Events From Profile {profile_name}", description=f"", color=0x8208d4)
    embed.add_field(name=f"Events of name '{event_name}' ({numEvents} total)\nPlease respond with the number of the event to be deleted\n(respond with any non number to cancel)", value="", inline=False)
    embed.set_footer(text=footer_text)
    
    await interaction.response.send_message(embed=embed)

    # Grabbing the users response 
    # function to check if the user responding is the same person who made the command and is responding from the same channel
    def check(m):
        return m.channel == interaction.channel and m.author == interaction.user
    
    reply = await client.wait_for("message", check=check)
    # Parsing the input
    try:
        num_reply = int(reply.content)
        if (num_reply > numEvents or num_reply < 1): raise ValueError("outside bounds")
    except ValueError:
        await bm.follow_up(interaction, f"Not a number between 1-{numEvents}") # Need to use a follow up after initial sending
        return

    chosen_event = eventsWithSameName[num_reply - 1]    # Grabbing the event that was chosen

    list_of_profiles = compare_and_delete(list_of_profiles, profile_name, chosen_event)

    dump_list_of_profiles(path, list_of_profiles)

    await bm.follow_up(interaction, "Event successfully deleted!")

async def google_calendar(interaction: discord.Interaction, profile_name: str):
    # Making sure the profile exists, and also grabbing the selected profile
    path = "scheduler/" + str(interaction.guild.id) + ".json"   # name of the file will be <guildID>.json and it will be located in the scheduler directory
    list_of_profiles = ret_list_of_profiles(path)

    # Checking if the profile exists
    if(profile_exists(profile_name, list_of_profiles) == 0):
        await bm.follow_up(interaction, "The profile you want to access does not exist!")
        return
    
    # Grabbing the selected profile
    selectedProfile = {}
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            selectedProfile = profile
    
    public_url = ""
    calendar_id = ""

    # Shows basic usage of the Google Calendar API.
    # The next 20 lines are from the Google Quickstart page on the google calendar api

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        request_body = {
            'summary': f"{profile_name}/{interaction.user.guild.name}",
            'timeZone': "America/Los_Angeles",
            'visibility': 'public'
        }

        # This will allow us to make the calendar public in order to allow us to take a screenshot of it with the selenium webdriver.
        rules = {
            "role": "reader",
            "scope": {
                "type": "default",
            }
        }
        
        response = service.calendars().insert(body=request_body).execute()
        calendar_id = response["id"]
        # Making the calendar public
        created_rule = service.acl().insert(calendarId=calendar_id, body=rules).execute()
        # Adding all the events to the calendar


        
        # this is the public url that will be returned by the function. 
        # Note that the ctz will always be the same as my account as it is by default set to America/Los_Angeles
        public_url = "https://calendar.google.com/calendar/embed?src=" + calendar_id + "&ctz=America%2FLos_Angeles"
        print(public_url)
        
        service.calendarList().delete(calendarId=calendar_id).execute()
    except HttpError as error:
        print('An error occurred: %s' % error)
    
    await get_screenshot(public_url)
    
    with open("myscreenshot.png", "rb") as f:
        screenshot = discord.File(f)
        await interaction.followup.send(f"{public_url}", file=screenshot)
    
    return

async def get_screenshot(url):
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.set_window_size(1920, 1100)
    size = driver.get_window_size()
    driver.get(url)
    

    # Clicking on the week tab to get the weekly schedule
    l=driver.find_element(By.ID, "tab-controller-container-week")
    driver.execute_script("arguments[0].click();", l)
    
    #Set the focus to the browser rather than the web content
    driver.set_context("chrome")
    #Create a var of the window
    win = driver.find_element_by_tag_name("window")
    #Send the key combination to the window itself rather than the web content to zoom out
    #(change the "-" to "+" if you want to zoom in)
    win.send_keys(Keys.CONTROL + "-")
    #Set the focus back to content to re-engage with page elements
    driver.set_context("content")
    
    sleep(1)
    

    driver.get_screenshot_as_file("myscreenshot.png")
    driver.quit()
    return

def disable_button(day_of_week, sunday_btn, monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, saturday_btn):
    # using day of week to know which button to disable
        if(day_of_week == 1):
            sunday_btn.disabled=False
            return
        elif(day_of_week == 2):
            monday_btn.disabled=False
            return
        elif(day_of_week == 3):
            tuesday_btn.disabled=False
            return
        elif(day_of_week == 4):
            wednesday_btn.disabled=False
            return
        elif(day_of_week == 5):
            thursday_btn.disabled=False
            return
        elif(day_of_week == 6):
            friday_btn.disabled=False
            return
        elif(day_of_week == 7):
            saturday_btn.disabled=False
            return

# returns a discord embed 
def return_embed_view_profile(profile_name, num_events, day_of_week, footer_text):
    embed=discord.Embed(title=f"Profile: {profile_name}", description=f"", color=0x8208d4)
    embed.add_field(name=f"({num_events}) events found on {ret_day_of_week(day_of_week)}", value="", inline=False)
    embed.set_footer(text=footer_text)
    return embed 

# Takes in a list of events and an integer from 1-7
# Returns the number of events found on that given day
def num_events_on_day(list_of_events, day_of_week):
    num_events = 0
    for event in list_of_events:
        if(event["day"] == day_of_week):
            num_events = num_events + 1
    return num_events

# Takes in a list of events and an integer from 1-7 
# returns a string containing the formatted form of all the events of a specific day
def grab_text_events_day(list_of_events, day_of_week):
    if(within_bounds(day_of_week, 1, 7) == 0):
        print("Error from grab_text_events_day: invalid day_of_week")
        return "ERROR"
        # Creating the footer text to be displayed on the embed by looping through the eventsWithSameName list, and adding the text of each event


    inc = 1     # incrementer to keep track of which number of profile we are on
    footer_text = ""
    for event in list_of_events:
        if(event["day"] == day_of_week):
            name = event["name"]
            note = event["notes"]
            start_hour = event["start_hour"]
            start_min = str(event["start_min"]) # setting the start_min as a string in order to utilize zfill method
            start_min = start_min.zfill(2)  # adding zeroes in front of the number until it's 2 digits long. For example, 1 becomes 01
            end_hour = event["end_hour"]
            end_min = str(event["end_min"]) # setting the end_min as a string in order to utilize zfill method
            end_min = end_min.zfill(2)    # adding zeroes in front of the number until it's 2 digits long. For example, 1 becomes 01
            string_day_of_week = ret_day_of_week(event["day"])

            footer_text = footer_text + f"{inc}: {name}\nNotes: {note}\nTime: {start_hour}:{start_min}-{end_hour}:{end_min}\nDay: {string_day_of_week}\n\n" 
            inc = inc+1

    return footer_text
    
    
# Takes a profilename and deletes the corresponding profile from the list of profiles
def delete_profile_from_list(list_of_profiles, profile_name):
    # looping through the list of profiles, and checking each of the profile names to see if a profile exists with the same name as the given name
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            list_of_profiles.remove(profile)
            return list_of_profiles
    return list_of_profiles

# Takes in the name of the profile and the list of all the profiles, searches through list of profiles and checks if a profile of the given name already exists
# returns a 0 if the profile doesn't exist, a 1 if it does
def profile_exists(name: str, list_of_profiles):
    # looping through the list of profiles, and checking each of the profile names to see if a profile exists with the same name as the given name
    for profile in list_of_profiles:
        if(profile["name"] == name):
            return 1
    return 0

# Takes in name of the profile, name of the event, and the list of profiles. Loops through list of profiles to find whether or not the event exists
# Returns 1 if an event with the given name exists, a 0 if it does not exist 
# Note: One should use the profile_exists function first before using this. 
def event_exists(profile_name:str, event_name:str, list_of_profiles):
    # looping through the list of profiles, and checking each of the profile names and stopping when we find the profile with the given name
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            for event in profile["events"]:
                if(event["name"] == event_name):
                    return 1
    return 0

# Takes a list of profiles, a profile name, and an event object (an event dictionary)
# Loops through the list of profiles until it gets to the profile with the given name, then loops through the events of that profile until the event with the exact same specifications 
# is reached then it is deleted from the list
# Returns the newly updated list of profile regardless of success 
def compare_and_delete(list_of_profiles, profile_name, chosen_event):
    for profile in list_of_profiles:
        if(profile["name"] == profile_name):
            for event in profile["events"]:
                if(event["name"] == chosen_event["name"] and 
                   event["notes"] == chosen_event["notes"] and 
                   event["start_hour"] == chosen_event["start_hour"] and
                   event["start_min"] == chosen_event["start_min"] and
                   event["end_hour"] == chosen_event["end_hour"] and
                   event["end_min"] == chosen_event["end_min"] and
                   event["day"] == chosen_event["day"]):
                    profile["events"].remove(event)
                    return list_of_profiles
    return list_of_profiles

# Takes in 3 integers as input
# makes sure that the number given as a parameter is less than or equal to the upper bound and greater than or equal to the lower bound
# returns 0 if the number is not within bounds, returns 1 if the number is within the bounds
def within_bounds(number: int, lowerBound: int, upperBound: int):
    if(number >= lowerBound and number <= upperBound):
        return 1
    else:
        return 0

# Function that takes the path to the file to be accessed and also the interaction object and returns a list of the profiles
def ret_list_of_profiles(path: str):    
    list_of_profiles = []

    # Reading JSON file and storing it in listObj as a list of dictionaries, each dictionary is a profile
    with open(path) as fp:
        list_of_profiles= json.load(fp)

    return list_of_profiles

# Function that takes a path to a json file and a list of dictionaries (the list of profiles) and writes the list to the json file
# This function exists in order to help minimize the code and make it more clean, as writing to the JSON is done multiple times. 
def dump_list_of_profiles(path: str, list_of_profiles):
    # dumping all of the profiles in the list in the JSON after having changed it 
            with open(path, "w") as f:
                json.dump(list_of_profiles, f, 
                        indent=2, 
                        separators=(",",": "))

# Given an integer returns the string form of the day of the week. 
def ret_day_of_week(day: int):
    if(day == 1):
        return "Sunday"
    elif(day == 2):
        return "Monday"
    elif(day == 3):
        return "Tuesday"
    elif(day == 4):
        return "Wednesday"
    elif(day == 5):
        return "Thursday"
    elif(day == 6):
        return "Friday"
    elif(day == 7):
        return "Saturday"

    return "ERROR"

# Returns an integer 1 if the event is valid, otherwise it returns an error string. 
def valid_event(start_hour, start_min, end_hour, end_min, day):
     # Checking if the given time values are within the needed bounds
    if(within_bounds(start_hour, 0, 23) == 0):
        return "Start hour time must be within 0 and 23 inclusive!"
    elif(within_bounds(start_min, 0, 59) == 0):
        return "Start minute time must be within 0 and 59 inclusive!"
    elif(within_bounds(end_hour, 0, 23) == 0):
        return "End hour time must be within 0 and 23 inclusive!"
    elif(within_bounds(end_min, 0, 59) == 0):
        return "End minute time must be within 0 and 59 inclusive!"
    elif(within_bounds(day, 1, 7) == 0):
        return "Day value must be within 1 and 7 inclusive!"
    # Making sure the end time is not actually before the end time (may mess with Google Calendar api)
    elif(end_hour < start_hour or (end_hour == start_hour and end_min <= start_min)):
        return "End time of the event should not be before or same as start time of the event!"
    
    return 1
