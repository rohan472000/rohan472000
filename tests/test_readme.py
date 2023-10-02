import unittest


class TestReadme(unittest.TestCase):

    def test_readme_contains_sections(self):
        with open('README.md', 'r', encoding='utf-8') as readme_file:
            readme_contents = readme_file.read()

        # Check for the "Connect with me👋" section
        self.assertIn(
            '<h2> Connect with me👋 </h2>',
            readme_contents,
            msg="README.md should contain 'Connect with me👋' section"
        )

        # Check for the "Visitor Count 👀" section
        self.assertIn(
            '<h2>Visitor Count 👀</h2>',
            readme_contents,
            msg="README.md should contain 'Visitor Count 👀' section"
        )

        # Check for the "Contributors 🌟" section
        self.assertIn(
            '## Contributors 🌟:',
            readme_contents,
            msg="README.md should contain 'Contributors 🌟' section"
        )

        # Check for the image link
        self.assertIn(
            '![Funny Meme](https://i.redd.it/81o7512qukrb1.jpg?width=100&height=100)',  # noqa: E501
            readme_contents,
            msg="README.md should contain the image link"
        )

        # Check for the warning about meme volatility
        self.assertIn(
            "Warning: The memes you see here are highly volatile and have a limited lifespan of 5 minutes. So, better hurry up and laugh before they disappear! 😄",  # noqa: E501
            readme_contents,
            msg="README.md should contain the meme volatility warning"
        )
