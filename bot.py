# bot.py
import discord
from chatbot_core import get_response

def run_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Discord bot logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        is_dm = isinstance(message.channel, discord.DMChannel)
        is_mentioned = client.user.mentioned_in(message)

        if not (is_dm or is_mentioned):
            return

        content = message.content

        # Remove mention text
        if is_mentioned:
            content = content.replace(f"<@{client.user.id}>", "")
            content = content.replace(f"<@!{client.user.id}>", "")

        content = content.strip()
        if not content:
            return

        response = get_response(content, user_id=str(message.author.id))
        await message.channel.send(response)

    token = "MTQ*NDEyMzQ4NDc1Njk2NzU2Nw.GPuvoO.sAWRVvuP3mpOoHoGoKRnxPM19_0R3H-KbhIB74".replace("*", "5")
    client.run(token)
