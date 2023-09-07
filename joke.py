#  Copyright (c) 2023 Rohan Anand (anand00rohan@gmail.com), rohan472000 on GitHub
import re

import requests
import json

# API endpoint to fetch memes from the "memes" subreddi, can give other api endpoint if you have any.
url = "https://www.reddit.com/r/memes/random.json?limit=1"
#url = "https://www.reddit.com/r/popular/random.json?limit=1"
#url = "https://v2.jokeapi.dev/joke/random.json?limit=1"
user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
# It will make a request to the Reddit API
response = requests.get(url, headers={'User-agent': user_agent})

# Now, Extract the  meme URL from the response JSON
data = json.loads(response.text)[0]['data']['children'][0]['data']
meme_url = data['url']
meme_url = data['url'] + "?width=100&height=100" # Add query string to reduce image size

# Create a Markdown image link with the meme URL
markdown = f"![Funny Meme]({meme_url})"

# Read the existing contents of README.md
with open('README.md', 'r') as file:
    lines = file.readlines()
    contents = []
    for i, line in enumerate(lines):
        if i+1 == len(lines):
            contents.append(line)
        elif line != '\n' or lines[i+1] != '\n':
            contents.append(line)

# Remove any existing meme Markdowns from the contents
contents = [line for line in contents if "![Funny Meme]" not in line]


# At Last, Write the Markdown to the README.md file
with open('README.md', 'w') as file:
    file.write(markdown + "\n\n")
    file.writelines(contents)
