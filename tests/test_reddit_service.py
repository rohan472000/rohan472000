import unittest
from unittest.mock import patch, MagicMock
import requests

from services.reddit import RedditService


class TestRedditService(unittest.TestCase):
    @patch("services.reddit.requests.get")
    def test_get_random_meme(self, mock_get):
        # Mock the response from the requests.get call
        mock_response = MagicMock()
        mock_response.status_code = 200  # A successful status code
        mock_response.json.return_value = [{
            "data": {"children": [{"data": {"url": "https://example.com/meme.jpg"}}]}
        }]
        mock_get.return_value = mock_response

        meme = RedditService.get_random_meme()

        self.assertEqual(meme, {"url": "https://example.com/meme.jpg"})

    @patch("services.reddit.requests.get")
    def test_get_random_meme_failure(self, mock_get):
        # Mock a request exception
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")
        meme_url = RedditService.get_random_meme()

        self.assertIsNone(meme_url)
