import discord



def run_discord_bot():
    TOKEN = 'MTA3MjcyNjQ3NzQyNDA1NDMyMg.G6Z8Sp.1rLmPMMR5ePOfFyJoxh7H801FX2VKMcN2pf1qo'
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents = intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author == client.user:
            return

        # Get data about the user
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # Debug printing
        print(f"{username} said: '{user_message}' ({channel})")

    # Remember to run your bot with your personal TOKEN
    client.run(TOKEN)