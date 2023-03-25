import pytest
import os
import json
import scheduler.schedule as sched

# White-box test
# This test provides 100%  Branch coverage for the ret_day_of_week function
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

# Acceptance Test
# Testing to make sure whether an event will be successfully deleted
def test_event_deletes():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    test_event_name = "TestEvent"
    test_event_notes = "TestEventNotes"
    
    list_of_profiles = init_test_events(test_profile_name, test_profile_notes, test_event_name, test_event_notes)
    chosen_event_class = sched.Event(test_event_name, test_event_notes, 1, 2, 0, 0, 1)  # Chosen event to be deleted will be exactly the same as the one in the list of profiles, as such it should be deleted by the compare_and_delete function
    
    new_list_of_profiles = sched.compare_and_delete(list_of_profiles, test_profile_name, chosen_event_class.__dict__)

    # Checking to see if the event was successfully deleted (init_test_profiles should return a profile with the same attributes as the profile in new_list_of_profiles)
    assert(new_list_of_profiles==init_test_profiles(test_profile_name, test_profile_notes))

# Acceptance Test
# Testing to make sure whether an event will successfully not be deleted 
def test_event_not_deleted():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    test_event_name = "TestEvent"
    test_event_notes = "TestEventNotes"
    
    list_of_profiles = init_test_events(test_profile_name, test_profile_notes, test_event_name, test_event_notes)
    chosen_event_class = sched.Event(test_event_name, test_event_notes, 12, 12, 13, 13, 5)  # Chosen event to be deleted will be an event that is not part of the list

    new_list_of_profiles = sched.compare_and_delete(list_of_profiles, test_profile_name, chosen_event_class.__dict__)

    # Checking to see if the event was successfully deleted (init_test_profiles should return a profile with the same attributes as the profile in new_list_of_profiles)
    assert(new_list_of_profiles==list_of_profiles)

# Acceptance Test
# Determining whether the profiles are able to be successfully deleted from the list_of_profiles
def test_profile_deleted():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    list_of_profiles = init_test_profiles(test_profile_name, test_profile_notes)
    new_list_of_profiles = sched.delete_profile_from_list(list_of_profiles, test_profile_name)
    
    # The new list should be empty after having deleted the only profile from the original list of profiles
    assert(new_list_of_profiles == [])
    return

# Acceptance Test
# Determining whether the ret_list_of_profiles function is successfully returning the correct list_of_profiles from a JSON file
def test_profile_not_deleted():
    test_profile_name = "TestName"
    test_profile_notes = "TestNotes"
    list_of_profiles = init_test_profiles(test_profile_name, test_profile_notes)
    new_list_of_profiles = sched.delete_profile_from_list(list_of_profiles, "NewTest")

    assert(new_list_of_profiles == list_of_profiles)


# White Box Test
# Testing to see if 2 numbers are within two bounds 
# This test provides full branch coverage 

# def within_bounds(number: int, lowerBound: int, upperBound: int):
#     if(number >= lowerBound and number <= upperBound):
#         return 1
#     else:
#         return 0

def test_within_bounds():
    # Number is between the upper and lower bounds
    assert(sched.within_bounds(10,5,15) == 1)
    # Number is smaller than lower bound
    assert(sched.within_bounds(4,5,15) == 0)
    # Number is larger than upper bound
    assert(sched.within_bounds(16,5,15) == 0)
    # upperbound is smaller than lowerbound
    assert(sched.within_bounds(10,15,5) == 0)

# White Box Test
# Testing to see if an event is valid. This test provides full 100% branch coverage

# def valid_event(start_hour, start_min, end_hour, end_min, day):
#      # Checking if the given time values are within the needed bounds
#     if(within_bounds(start_hour, 0, 23) == 0):
#         return "Start hour time must be within 0 and 23 inclusive!"
#     elif(within_bounds(start_min, 0, 59) == 0):
#         return "Start minute time must be within 0 and 59 inclusive!"
#     elif(within_bounds(end_hour, 0, 23) == 0):
#         return "End hour time must be within 0 and 23 inclusive!"
#     elif(within_bounds(end_min, 0, 59) == 0):
#         return "End minute time must be within 0 and 59 inclusive!"
#     elif(within_bounds(day, 1, 7) == 0):
#         return "Day value must be within 1 and 7 inclusive!"
#     # Making sure the end time is not actually before the end time (may mess with Google Calendar api)
#     elif(end_hour < start_hour or (end_hour == start_hour and end_min <= start_min)):
#         return "End time of the event should not be before or same as start time of the event!"
    
#     return 1
def test_event_invalid():
    # Valid event
    assert(sched.valid_event(12, 20, 13, 20, 5) == 1)
    # Invalid start hour time
    assert(sched.valid_event(24, 10, 23, 10, 5) == "Start hour time must be within 0 and 23 inclusive!")
    # Invalid start min time
    assert(sched.valid_event(20, 100, 23, 10, 5) == "Start minute time must be within 0 and 59 inclusive!")
    # Invalid end hour time
    assert(sched.valid_event(12, 10, 25, 10, 5) == "End hour time must be within 0 and 23 inclusive!")
    # Invalid end min time
    assert(sched.valid_event(12, 10, 13, 100, 5) == "End minute time must be within 0 and 59 inclusive!")
    # Invalid day
    assert(sched.valid_event(12, 10, 13, 10, 8) == "Day value must be within 1 and 7 inclusive!")
    # start event time is after end event time
    assert(sched.valid_event(12, 10, 11, 10, 5) == "End time of the event should not be before or same as start time of the event!")

# Integration Test
# Big Bang Integration Test testing the combination of profile and event classes and whether they can be effectively turned into dictionaries
def test_profile_and_event_integration():
    profile_with_event = {
        "name": "TestName",
        "notes": "TestNotes",
        "events": [
            {
                "name": "TestEvent",
                "notes": "TestEventNotes",
                "start_hour": 12,
                "start_min": 30,
                "end_hour": 13,
                "end_min": 30,
                "day": 1
            }
        ]
    } 

    test_profile = sched.Profile("TestName", "TestNotes", [sched.Event("TestEvent", "TestEventNotes", 12, 30, 13, 30, 1)])
    test_profile_dict = test_profile.__dict__
    
    assert(test_profile_dict == profile_with_event)


# NOT A TEST FUNCTION
# Returns a list of profiles with a single profile with the given name and notes, profile will have an empty events list
def init_test_profiles(profile_name, profile_notes):
    list_of_profiles = []
    profile = sched.Profile(profile_name, profile_notes, [])
    list_of_profiles.append(profile.__dict__)
    return list_of_profiles

# NOT A TEST FUNCTION
# Returns a list with a single profile which contains a single event in its events list
def init_test_events(profile_name, profile_notes, event_name, event_notes):
    list_of_profiles = init_test_profiles(profile_name, profile_notes)
    event = sched.Event(event_name, event_notes, 1, 2, 0, 0, 1)
    # Adding the profile to the list
    list_of_profiles[0]["events"].append(event.__dict__)

    return list_of_profiles


