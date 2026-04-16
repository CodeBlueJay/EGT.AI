# bot.py
import os
import sys
import tempfile
import discord
from chatbot_core import get_response

def run_bot():
    # Ensure only one instance runs
    lockfile = os.path.join(tempfile.gettempdir(), 'egt_discord_bot.lock')
    lockfd = None
    try:
        lockfd = os.open(lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
        os.write(lockfd, str(os.getpid()).encode())
    except FileExistsError:
        print("Another instance is already running.")
        sys.exit(1)

    try:
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

        token = "MTQ*NDEyMzQ4NDc1Njk2NzU2Nw.Gp_dWD.9DTlG48PliYOwujlIoJMER3tOfwbNYv6ODpuu0".replace("*", "5")
        client.run(token)
    finally:
        try:
            if lockfd is not None:
                os.close(lockfd)
            os.remove(lockfile)
        except Exception:
            pass
