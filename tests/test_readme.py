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
