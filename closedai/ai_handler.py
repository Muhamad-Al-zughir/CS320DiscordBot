# shbang
# Judah Tanninen
# In between handler for discord to openai

# Imports
import closedai.ai as ai
import discord

# Basic image generation function, takes in a prompt, as well as a number of results
# Returns an array of urls to the generated images
# If error occurs while generating images, function will return false
def genImages(prompt, results):

    # Attempt to create some images, wrap attempt in a try so we can detect errors and alert the user
    try:
        res = ai.basicImage(prompt, results)
        data = res['data']
        urls = []
        # Loop through the data list and create a list of urls
        for val in data:
            url = val['url']
            urls.append(url)
        return urls
    except:
        return False

# Basic completion function, takes in the messages array, as well as the current settings, and runs a completion on them
# Returns a dict, with the following keys: completions, in_tokens, out_tokens.
# completions is an array of dicts, which contain text, index, logprobs, and finish_reason
def getCompletion(messages, settings):
    # Pull the variables out from the settings
    temp = settings['temp']
    results = settings['results']
    maxTokens = settings['maxTokens']
    # Make a call to the basic completion, should return the api response
    try:
        res = ai.basicCompletion(messages, temp, results, maxTokens)
        # Res should contain multiple things, see https://platform.openai.com/docs/api-reference/completions/create
        resDict = {
            'completions': res['choices'],
            'in_tokens': res['usage']['prompt_tokens'],
            'out_tokens': res['usage']['completion_tokens'],
        }
        return resDict
    except:
        return False

# Basic function, lists of all available openai models
def getModels():
    # Get a list of all models. NOTE: this is more for a test than actual functionality
    models = ai.listModels()
    list = models.data
    str = ''
    names = []
    # Loop over the list, adding all the ids (names) to an array (could also map)
    for val in list:
        name = val['id']
        names.append(name)
    str = ", ".join(names)
    return str

###########################
# HANDLER FUNCTIONS
###########################

## Adds three backticks to any given string, turning it into a code string for the discord
# This makes it look cooler essentially
def codefiy(str):
    newStr = f"```{str}```"
    return newStr

# Takes in a string, converts it to either an integer, or, if needed, a float
def convertToFloatOrInt(str):
    # Wrap returning of int casting in a try. If it fails, cast to float instead
    try:
        return int(str)
    except ValueError:
        return float(str)
    
# Sends the response as a nice string to the discord, put here to keep the client.py file as small as possible.
async def sendResponses(interaction, completion, settings):
    # Now that we have the res, we need to handle it by turning it into a cool little string
    # We will be breaking the response into two responses, one for the usage, one for the completions
    usageStr = '**Usage**:\n'
    usage = genUsageStr(settings, completion)
    coolUsage = codefiy(usage)
    usageStr += coolUsage
    await interaction.followup.send(usageStr)

    # Now we send the completions
    compStr = '**Completion(s)**\n'
    comp = genCompletionsStr(completion['completions'])
    compStr += comp

    # Attempt to send the completion string to the discord
    try:
        await interaction.followup.send(compStr)
    except: # IF IT FAILS, create an output md file, then send that instead.
        genOutFile(compStr) # Create/overwrite the file
        await interaction.followup.send( # Send the response, with an output file instead of the normal response
            content="**Response over 2k characters, creating output file**",
            file=discord.File('output.md'),
        )


# For when the response from gpt is over 2k characters, we will need to send a file instead.
# File should be a .md file so the markdown is respected.
def genOutFile(str):
    # Create a file
    f = open('output.md', 'w') # Should empty the file
    # Write the output string to the file
    f.write(str)
    # Close the file
    f.close()


# Takes in the settings and completion response, and does some work to make a little string
# for the discord to get
def genUsageStr(settings, completion):
    str = ''
    str += f"in_tokens: {completion['in_tokens']}\n"
    str += f"out_tokens: {completion['out_tokens']}\n"
    
    # Loop through the settings, add them all to the string
    for key in settings:
        newStr = f"{key}: {settings[key]}"
        str += f"\n{newStr}"
    return str

# Takes in the array of completions, does some work to make a nice little string for the discord
# Note, returns just one string, not an array of strings, 
# Double note, strings that need codefied are already wrapped.
def genCompletionsStr(completions):
    str = '' # Create the og string

    # Loop through all the completions, adding their content to the string
    for val in completions: # Note that usually there will only be one completion
        text = val['message']['content']
        reason = val['finish_reason']
        str += text
        str += f"\n*Finish Reason: {reason}*\n\n"
    return str

def genConvoItem(prompt):
    return {
        "role": "user",
        "content": prompt
    }

async def sendCaiOptions(interaction):
    str = '**Closed AI Options**\n'
    str += "listmodels: Visual Only, lists all current models availble to the completion API, for testing only\n"
    str += "listsettings: Lists the current settings for the cai gpt completions\n"
    str += "changesetting: Change any of the settings listed in the listsettings function\n"
    str += "caioptions: This function.\n"
    str += "caigpt: Essentially chatgpt, uses the gpt-3.5-turbo model, takes in prompts and keeps track of the conversation. Uses the settings listed in listsettings\n"
    str += "dalle: DALL-E image generation, generates n number of images for the given prompt\n"
    await interaction.response.send_message(str)
    