import json
import discord
from discord.ui import Button, View
from datetime import time


async def list_profiles(interaction: discord.Interaction):
    embed=discord.Embed(title="Profiles", description="All schedules in the server ")
    embed.add_field(name="Page 1/20", value="", inline=False)
    embed.set_footer(text="Joe\nMuhamad\nJudah\nShawyan\nAlex")

    # function is called whenever the left arrow button is clicked
    async def left_arrow_callback(interaction):
        await interaction.response.send_message("Left arrow has been clicked!")
    async def right_arrow_callback(interaction):
        await interaction.response.send_message("Right arrow has been clicked!")
    
    # creating the buttons
    left_arrow = Button(label="🡠")
    left_arrow.callback = left_arrow_callback

    right_arrow = Button(label="🡢")
    right_arrow.callback = right_arrow_callback

    # Creating the view to display the buttons
    view = View()
    view.add_item(left_arrow)
    view.add_item(right_arrow)
    await interaction.response.send_message(embed=embed, view=view)
