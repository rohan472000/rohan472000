import requests
import json

# Reddit API endpoint to fetch memes from the "memes" subreddit
url = "https://www.reddit.com/r/memes/random.json?limit=1"

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
# Make a request to the Reddit API
response = requests.get(url, headers={'User-agent': user_agent})

# Extract the meme URL from the response JSON
data = json.loads(response.text)[0]['data']['children'][0]['data']
meme_url = data['url']
meme_url = data['url'] + "?width=50&height=50" # Add query string to reduce image size

# Create a Markdown image link with the meme URL
markdown = f"![Funny Meme]({meme_url})"

# Read the existing contents of README.md
with open('README.md', 'r') as file:
    contents = file.readlines()

# Remove any existing meme Markdowns from the contents
contents = [line for line in contents if "![Funny Meme]" not in line]

# Write the Markdown to the README.md file
with open('README.md', 'w') as file:
    file.write(markdown + "\n\n")
    file.writelines(contents)
