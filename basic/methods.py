
async def send_msg(interaction, in_string: str):
    await interaction.response.send_message(in_string)

async def follow_up(interaction, in_string: str):
    await interaction.followup.send(in_string)