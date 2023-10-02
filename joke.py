import requests
import logging
import re
import json

# Constants
REDDIT_API_URL = "https://www.reddit.com/r/memes/random.json?limit=1"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)
README_FILE = 'README.md'
IMAGE_EXTENSIONS_PATTERN = re.compile(r'\.(jpg|jpeg|png)$', re.IGNORECASE)

# Configure logging
logging.basicConfig(level=logging.INFO)


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


def update_readme_with_url(markdown):
    try:
        with open(README_FILE, 'r') as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Funny Meme]" in line:
                contents[i] = markdown + "\n"
                break

        with open(README_FILE, 'w') as file:
            file.writelines(contents)
    except (IOError, FileNotFoundError) as e:
        logging.error(f"An error occurred: {e}")


def main():
    meme_url = fetch_random_url(REDDIT_API_URL, USER_AGENT)
    if meme_url and IMAGE_EXTENSIONS_PATTERN.search(meme_url):
        markdown = f"![Funny Meme]({meme_url}?width=100&height=100)"
        update_readme_with_url(markdown)


if __name__ == "__main__":
    main()
