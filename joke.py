import json
import logging
import re
from typing import Dict, Union
from bs4 import BeautifulSoup as bs

import requests

# Constants
REDDIT_API_URL = "https://www.reddit.com/r/memes/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)
README_FILE = "README.md"
IMAGE_EXTENSIONS_PATTERN = re.compile(r"\.(jpg|jpeg|png)$", re.IGNORECASE)

# Configure logging
logging.basicConfig(level=logging.INFO)


def fetch_random_meme(api_url: str, user_agent: str) -> Union[None, Dict[str, None]]:
    """Get URL and Author of a random meme from Reddit API."""
    try:
        response = requests.get(api_url, headers={"User-agent": user_agent})
        response.raise_for_status()
        response = response.json()[0]["data"]["children"][0]["data"]
        return {
            "url": response.get("url"),
            "author": response.get("author")
        } 
    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError,
        IndexError,
    ) as e:
        logging.error(f"An error occurred: {e}")
        return None


def update_readme(url: str, author: Union[str, None] = None) -> bool:
    """Update README with new URL, returning whether successful."""
    try:
        with open(README_FILE, "r") as file:
            contents = file.read()

        soup = bs(contents, "html.parser")
        joke_img_tag = soup.find("img", {"id": "joke"})
        if joke_img_tag:
            joke_img_tag["src"] = url
            joke_img_tag["title"] = f"u/{author}" if author else "null"

        with open(README_FILE, "w") as file:
            file.write(str(soup))

        return True
    except (IOError, FileNotFoundError) as e:
        logging.error(f"An error occurred: {e}")
        return False


def main() -> None:
    """Update README with a new meme."""
    meme = fetch_random_meme(REDDIT_API_URL, USER_AGENT)
    if meme:
        url, author = meme.get("url"), meme.get("author")
        if url and IMAGE_EXTENSIONS_PATTERN.search(url):
            update_readme(url, author)


if __name__ == "__main__":
    main()
