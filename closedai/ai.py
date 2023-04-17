# shbang
# Judah Tanninen
# Functions that directly can be called to use the openai functionality

# Imports
import openai
import os
from dotenv import load_dotenv

# Get the api key needed to interface with openai
# NOTE: THIS SHIT COSTS MONEY, its pretty cheap, but don't be putting calls to openai in a loop
load_dotenv() # loads all the content in the .env folder
TOKEN = os.getenv('OPENAI_KEY')
openai.api_key = TOKEN

# Basic function which returns the models available to openai
# Note that we do not have the ability to use all of these.
# Use the discord command "list_abilities" to get the abilities of the bot
def listModels():
    models = openai.Model.list()
    return models

# Basic completion call, takes in some parameters, makes a call to openai, then returns the response
def basicCompletion(messages, temp, results, maxTokens):
    # Make a completion (basically just inputs text and gets text in response)
    completion = openai.ChatCompletion.create(
        messages=messages,
        temperature=temp,
        n=results,
        max_tokens=maxTokens,
        model='gpt-3.5-turbo'
    )
    return completion

def basicImage(prompt, results):
    response = openai.Image.create(
        prompt=prompt, 
        n=results, 
        size="1024x1024"
    )
    return response
