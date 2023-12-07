# Discord Bot Invitation Link: https://discord.com/api/oauth2/authorize?c
# lient_id=1158445141066002432&permissions=274877942784&scope=bot

import discord
from discord.ext import commands
import os
from collections import deque

from services.reddit import RedditService

# TOKEN = os.environ.get("DISCORD")
TOKEN = os.getenv("DISCORD")
# TOKEN = '${{ secrets.DISCORD }}'
# print("token initials are : ", TOKEN)

# Define intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

sent_memes = deque(maxlen=10)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.command()
async def postmeme(ctx):
    meme_url = fetch_random_url()

    if meme_url:
        if meme_url not in sent_memes:
            sent_memes.append(meme_url)
            await ctx.send(f"Here's a funny meme for you: {meme_url}")
        else:
            await ctx.send("I've already sent this meme recently!")


def fetch_random_url():
    random_meme = RedditService.get_random_meme()
    if random_meme:
        random_meme_url = random_meme["url"]
    else:
        random_meme_url = None
    return random_meme_url


bot.run(TOKEN)
