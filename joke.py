import json
import logging
import re
from typing import Optional

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


def fetch_random_meme(api_url: str, user_agent: str) -> Optional[dict]:
    """Get data of a random meme from Reddit API."""
    try:
        response = requests.get(api_url, headers={"User-agent": user_agent})
        response.raise_for_status()
        data = response.json()[0]["data"]["children"][0]["data"]
        return {"url": data["url"], "author": data["author"]}
    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError,
        IndexError,
    ) as e:
        logging.error(f"An error occurred: {e}")
        return None


def update_readme_with_meme(markdown: dict) -> bool:
    """Update README with new meme data, returning whether successful."""
    try:
        with open(README_FILE, "r") as file:
            readme_contents = file.read()

        updated_contents = readme_contents.replace(
            "![Funny Meme]", markdown["url"]
        ).replace("Meme Author", markdown["author"])

        with open(README_FILE, "w") as file:
            file.write(updated_contents)
        return True
    except (IOError, FileNotFoundError) as e:
        logging.error(f"An error occurred: {e}")
        return False


def main() -> None:
    """Update README with a new meme."""
    meme_data = fetch_random_meme(REDDIT_API_URL, USER_AGENT)
    if meme_data and IMAGE_EXTENSIONS_PATTERN.search(meme_data["url"]):
        markdown = {
            "url": f"![Funny Meme]({meme_data['url']}?width=100&height=100)",
            "author": f"* Meme Author: [{meme_data['author']}](https://www.reddit.com/user/{meme_data['author']}/)",
        }
        update_readme_with_meme(markdown)


if __name__ == "__main__":
    main()
    