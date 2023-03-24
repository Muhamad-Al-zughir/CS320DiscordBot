import pytest
import os
import json
import scheduler.schedule as sched

# White-box test
# This test provides 100% coverage for the ret_day_of_week function
# Tests values 1-7, along with values greater than 7 and less than 1

# Given an integer returns the string form of the day of the week. 
# def ret_day_of_week(day: int):
#     if(day == 1):
#         return "Sunday"
#     elif(day == 2):
#         return "Monday"
#     elif(day == 3):
#         return "Tuesday"
#     elif(day == 4):
#         return "Wednesday"
#     elif(day == 5):
#         return "Thursday"
#     elif(day == 6):
#         return "Friday"
#     elif(day == 7):
#         return "Saturday"

#     return "ERROR"

def test_ret_day_of_week():
    assert(sched.ret_day_of_week(0) == "ERROR")
    assert(sched.ret_day_of_week(1) == "Sunday")
    assert(sched.ret_day_of_week(2) == "Monday")
    assert(sched.ret_day_of_week(3) == "Tuesday")
    assert(sched.ret_day_of_week(4) == "Wednesday")
    assert(sched.ret_day_of_week(5) == "Thursday")
    assert(sched.ret_day_of_week(6) == "Friday")
    assert(sched.ret_day_of_week(7) == "Saturday")
    assert(sched.ret_day_of_week(8) == "ERROR")

# Acceptance Test
# Test to make sure we can effectively detect whether a profile does exist within a JSON
def test_profile_exists():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    list_of_profiles = init_test_profiles(test_profile_name, test_profile_notes)

    # Checking if a profile which should exist exists in the list of profiles using the profile_exists function
    assert(sched.profile_exists(test_profile_name, list_of_profiles) == 1)

# Acceptance Test
# Test to make sure we can effectively detect whether a profile doesn't exist within a JSON
def test_profile_does_not_exist():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    list_of_profiles = init_test_profiles(test_profile_name, test_profile_notes)

    # checking if a profile of the name "NewTestName" (which should not exist) exists in the list using the profile_exists function 
    assert(sched.profile_exists("NewTestName", list_of_profiles) == 0)

# Acceptance Test
# Test to make sure we can effectively detect whether an event exists within a profile in a JSON file
def test_event_exists():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    test_event_name = "TestEvent"
    test_event_notes = "TestEventNotes"

    list_of_profiles = init_test_events(test_profile_name, test_profile_notes, test_event_name, test_event_notes)

    # Checking if an event exists when it should exist
    assert(sched.event_exists(test_profile_name, test_event_name, list_of_profiles) == 1)
    
# Acceptance Test
# Test to make sure we can effectively detect whether an event does not exist within a profile in a JSON file
def test_event_does_not_exist():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    test_event_name = "TestEvent"
    test_event_notes = "TestEventNotes"

    list_of_profiles = init_test_events(test_profile_name, test_profile_notes, test_event_name, test_event_notes)

    # Checking if an event exists when it should NOT exist
    assert(sched.event_exists(test_profile_name, "NewTestEvent", list_of_profiles) == 0)

# Returns a list of profiles with a single profile with the given name and notes, profile will have an empty events list
def init_test_profiles(profile_name, profile_notes):
    list_of_profiles = []
    profile = sched.Profile(profile_name, profile_notes, [])
    list_of_profiles.append(profile.__dict__)
    return list_of_profiles

# Returns a list with a single profile which contains a single event in its events list
def init_test_events(profile_name, profile_notes, event_name, event_notes):
    list_of_profiles = init_test_profiles(profile_name, profile_notes)
    event = sched.Event(event_name, event_notes, 1, 2, 0, 0, 1)
    # Adding the profile to the list
    list_of_profiles[0]["events"].append(event.__dict__)

    return list_of_profiles


