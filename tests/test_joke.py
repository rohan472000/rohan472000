import unittest
from unittest.mock import patch
import requests
from joke import fetch_random_meme


class TestJokeFunctions(unittest.TestCase):

    @patch('joke.requests.get')
    def test_fetch_random_url_success(self, mock_get):
        # Mock the response from the requests.get call
        mock_response = {
            "data": {
                "children": [
                    {
                        "data": {
                            "url": "https://example.com/meme.jpg"
                        }
                    }
                ]
            }
        }
        mock_get.return_value.json.return_value = [mock_response]

        meme = fetch_random_meme(
            "https://www.reddit.com/r/memes/random.json?limit=1",
            "Test User Agent")

        self.assertEqual(meme.get("url"), "https://example.com/meme.jpg")

    @patch('joke.requests.get')
    def test_fetch_random_url_failure(self, mock_get):
        # Mock a request exception
        mock_get.side_effect = requests.exceptions.RequestException(
            "Request failed"
        )
        meme = fetch_random_meme("https://www.reddit.com/r/memes/random.json?limit=1", "Test User Agent")  # noqa: E501

        self.assertIsNone(meme)
