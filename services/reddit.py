import logging
import requests
from typing import Optional, Dict
import json


class RedditService:
    REDDIT_API_RANDOM_MEME_URL = "https://www.reddit.com/r/memes/random.json?limit={limit}"
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    )

    @classmethod
    def get_random_meme(cls) -> Optional[Dict]:
        """Get random meme from Reddit."""

        api_url = cls.REDDIT_API_RANDOM_MEME_URL.format(limit=1)
        try:
            response = requests.get(api_url, headers={"User-agent": cls.USER_AGENT})
            response.raise_for_status()

            if response.status_code < 200 or response.status_code >= 300:
                logging.error(f"Reddit API request failed with status code {response.status_code}")
                return None

            return response.json()[0]["data"]["children"][0]["data"]
        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError, IndexError) as e:
            logging.error(f"An error occurred: {e}")
            return None
