import logging
import re
from typing import Optional

from services.reddit import RedditService

# Constants
README_FILE = "README.md"
IMAGE_EXTENSIONS_PATTERN = re.compile(r"\.(jpg|jpeg|png)$", re.IGNORECASE)
TIMEOUT = 5 # Timeout( seconds)

# Configure logging
logging.basicConfig(level=logging.INFO)


def fetch_random_meme() -> Optional[dict]:
    """Get a random meme data from Reddit API."""
    try:
        meme = RedditService.get_random_meme(timeout=TIMEOUT)
        if meme and IMAGE_EXTENSIONS_PATTERN.search(meme["url"]):
            return meme
    except TimeoutError as err:
        logging.error(f"Fetching meme timed out: {err}")
    return None


def update_readme_with_meme(meme: dict) -> bool:
    """Update README with meme data, returning whether successful."""
    try:
        with open(README_FILE, "r") as file:
            contents = file.readlines()

        for i, line in enumerate(contents):
            if "![Funny Meme]" in line:
                # Remove the previous author line
                if i + 1 < len(contents) and contents[i + 1].startswith("* Meme Author:"):
                    del contents[i + 1]

                meme_url = meme["url"]
                meme_author = meme["author"]
                markdown = f"![Funny Meme]({meme_url}?width=100&height=100)\n"
                markdown += f"* Meme Author: [{meme_author}](https://www.reddit.com/user/{meme_author}/)\n"
                contents[i] = markdown
                break

        with open(README_FILE, "w") as file:
            file.writelines(contents)
        return True
    except (IOError, FileNotFoundError) as e:
        logging.error(f"An error occurred: {e}")
        return False


def main() -> None:
    """Update README with a new meme."""
    meme = fetch_random_meme()
    if meme and IMAGE_EXTENSIONS_PATTERN.search(meme["url"]):
        update_readme_with_meme(meme)


if __name__ == "__main__":
    main()
