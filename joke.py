import argparse
import json
import logging
import re
from io import BytesIO
from typing import Optional

import PIL
import requests
from PIL import Image

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


def show_meme_image(meme_url: str) -> None:
    try:
        response = requests.get(meme_url)
        response.raise_for_status()
        image_bytes = BytesIO(response.content)
        image = Image.open(image_bytes)
        image.show()
    except (
        requests.exceptions.RequestException,
        PIL.UnidentifiedImageError,
    ) as e:
        logging.error(f"An error occurred: {e}")


def save_meme_image(meme_url: str, output_filename: str) -> None:
    try:
        response = requests.get(meme_url)
        response.raise_for_status()
        with open(output_filename, "wb") as file:
            file.write(response.content)
        logging.info(f"Meme image saved to {output_filename}")
    except (requests.exceptions.RequestException, IOError) as e:
        logging.error(f"An error occurred: {e}")

def init_args():
    """Initialize and parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Fetch and display a random meme from Reddit.")
    parser.add_argument("--show", action="store_true", help="Display the meme image.")
    parser.add_argument("--save", action="store_true", help="Save the meme image to a file.")
    parser.add_argument("--output", type=str, help="Specify the output filename for the saved image.")
    return parser.parse_args()

def main() -> None:
    """Update README with a new meme and optionally show/save the meme image."""
    args = init_args()

    meme_url = fetch_random_url(REDDIT_API_URL, USER_AGENT)
    if meme_url and IMAGE_EXTENSIONS_PATTERN.search(meme_url):
        markdown = f"![Funny Meme]({meme_url}?width=100&height=100)"
        update_readme_with_url(markdown)

        if args.show:
            show_meme_image(meme_url)

        if args.save and args.output:
            save_meme_image(meme_url, args.output)

if __name__ == "__main__":
    main()
