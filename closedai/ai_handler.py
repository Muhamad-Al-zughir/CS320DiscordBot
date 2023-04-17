# shbang
# Judah Tanninen
# In between handler for discord to openai

# Imports
import closedai.ai as ai


# Basic completion function, takes in a prompt, as well as the current settings, and runs a completion on them
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
    await  interaction.followup.send(compStr)

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