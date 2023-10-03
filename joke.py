import json
import logging
import re
from typing import Optional

import requests

import os

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


def post_comment(pr_url, meme_url, token):
    """Add meme comment meme on PR."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    comment = {
        "body": f"![Meme]({meme_url})"
    }
    response = requests.post(pr_url, headers=headers, data=json.dumps(comment))
    if response.status_code != 201:
        logging.error(f"Failed to post comment: {response.text}")
        

def fetch_random_url(api_url: str, user_agent: str) -> Optional[str]:
    """Get URL of a random meme from Reddit API."""
    try:
        response = requests.get(api_url, headers={"User-agent": user_agent})
        response.raise_for_status()
        return response.json()[0]["data"]["children"][0]["data"]["url"]
    except (
        requests.exceptions.RequestException,
        json.JSONDecodeError,
        KeyError,
        IndexError,
    ) as e:
        logging.error(f"An error occurred: {e}")
        return None


def update_readme_with_url(markdown: str) -> bool:
    """Update README with new URL, returning whether successful."""
    try:
        with open(README_FILE, "r") as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Funny Meme]" in line:
                contents[i] = markdown + "\n"
                break

        with open(README_FILE, "w") as file:
            file.writelines(contents)
        return True
    except (IOError, FileNotFoundError) as e:
        logging.error(f"An error occurred: {e}")
        return False


def main() -> None:
    # """Update README with a new meme."""
    """Add meme comment on PR"""
    
    meme_url = fetch_random_url(REDDIT_API_URL, USER_AGENT)
    if meme_url and IMAGE_EXTENSIONS_PATTERN.search(meme_url):
        # markdown = f"![Funny Meme]({meme_url}?width=100&height=100)"
        # update_readme_with_url(markdown)
        token = os.environ.get("GITHUB_TOKEN")
        pr_url = os.environ.get("PR_URL")
        if token and pr_url:
            post_comment(pr_url, meme_url, token)
        else:
            logging.error("GITHUB_TOKEN or PR_URL environment variables are missing")


if __name__ == "__main__":
    main()
