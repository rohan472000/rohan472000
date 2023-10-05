# Discord Bot Invitation Link: https://discord.com/api/oauth2/authorize?c
# lient_id=1158445141066002432&permissions=274877942784&scope=bot

import discord
from discord.ext import commands
import requests
import logging
import json
import os
from collections import deque
# Constants
REDDIT_API_URL = "https://www.reddit.com/r/memes/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)


TOKEN = os.environ.get("DISCORD")
print("token initials are : ", TOKEN)

# Define intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


sent_memes = deque(maxlen=10)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


@bot.command()
async def postmeme(ctx):
    meme_url = fetch_random_url(REDDIT_API_URL, USER_AGENT)

    if meme_url:
        if meme_url not in sent_memes:
            sent_memes.append(meme_url)
            await ctx.send(f"Here's a funny meme for you: {meme_url}")
        else:
            await ctx.send("I've already sent this meme recently!")


def fetch_random_url(api_url, user_agent):
    try:
        response = requests.get(api_url, headers={'User-agent': user_agent})
        response.raise_for_status()
        return response.json()[0]['data']['children'][0]['data']['url']
    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError,
        IndexError
    ) as e:
        logging.error(f"An error occurred: {e}")
        return None


bot.run(TOKEN)
