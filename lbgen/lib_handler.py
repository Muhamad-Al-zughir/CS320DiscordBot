import lbgen.lib as libby
import basic.methods as bm
from discord.ui import View, Button
import discord

async def handleLibSearch(interaction, type, search):
    res = libby.handleValidation(type, search)
    # We want to always send something, so discord doesn't time us out.
    if (res != True):
            await bm.send_msg(interaction, res)
            return
    else:
        await bm.send_msg(interaction, 'Beginning Search...')
    # All messages after this point should be sent as followups

    # Make a basic search to libgen
    results = libby.basicSearch(type, search)
    # Check the length of the results, if no results, alert the users, and return
    if (len(results) == 0):
        await bm.follow_up(interaction, "Search returned no results, try another combination")
        return

    # Format the results into an array of results
    strings = libby.formatResults(results)
    msg = '\n'.join(strings) # Turn into one string
    # Create some buttons for the user to use
    buttons = genButtonList(results)
    # Create a new view for us to add these wonderful little buttons to, big pog
    view = View()

    # Loop through all buttons, and add them all to the 
    for i in range(len(buttons)):
        view.add_item(buttons[i])
    await interaction.followup.send(content=msg, view=view)

# Generates a list of buttons, from 1 - len
def genButtonList(results):
    resultLen = len(results)
    # Create a callback for the buttons to hit
    buttons = []
    for i in range(resultLen):
        label = str(i + 1)
        # Instantiate the result select button, which has a specific callback for result selection
        btn = resultSelectBtn(label, results)
        buttons.append(btn)
    return buttons

############################
## CLASSES
############################


# New Result select button, extends the button class
# Takes in a button name, and a list of results that will be selected from 
class resultSelectBtn(Button):
    # Constructor for button
    def __init__(self, buttonName, results):
        super().__init__(
            label=buttonName,
            custom_id=buttonName,
            style=discord.ButtonStyle.blurple
        )
        self.results = results
    
    # Callback for function
    # Gets the links for the selected book, and creates a message with the links as buttons.
    # It also states how many links it is returning in its message.
    async def callback(self, interaction):
        await bm.send_msg(interaction, 'Searching for links...')
        id = self.custom_id
        # Get the chosen result from the list of resultks
        chosen = int(id)
        obj = self.results[chosen - 1]
        # Get all the links for the chosen result
        links = libby.getLinksFor(obj)
        # Create some buttons for the links
        view = View()

        # Loop through all the links, and create a cool url button for each link
        for key in links:
            # Create a simple button, making use of the url functionality
            btn = Button(label=key, url=links[key])
            view.add_item(btn)
        # Little message telling the users how many links there are for the book.
        msg = f"Found ({len(links)}) links for the selected title: {obj['title']}"
        await interaction.followup.send(content=msg, view=view)
