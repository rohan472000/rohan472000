#  Copyright (c) 2023 Rohan Anand (anand00rohan@gmail.com), rohan472000 on GitHub
import requests
import json

# Reddit API endpoint to fetch memes from the "memes" subreddit, can give other api endpoint if you have any.
#url = "https://www.reddit.com/r/memes/random.json?limit=1"
url = "http://icanhazdadjoke.com?limit=1"

user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
# Make a request to the Reddit API
response = requests.get(url, headers={'User-agent': user_agent})

# Extract the  meme URL from the response JSON
data = json.loads(response.text)[0]['data']['children'][0]['data']
meme_url = data['url']
meme_url = data['url'] + "?width=100&height=100" # Add query string to reduce image size

# Create a Markdown image link with the meme URL
markdown = f"![Funny Meme]({meme_url})"

# Read the existing contents of README.md
with open('README.md', 'r') as file:
    contents = file.readlines()

# Remove any existing meme Markdowns from the contents
contents = [line for line in contents if "![Funny Meme]" not in line]

# Write the Markdown to the README.md file
with open('README.md', 'w') as file:
    # Add the warning message if it does not exist
#     if contents[0].strip() != "## Warning: The memes you see here are highly volatile and have a limited lifespan of 5 minutes. So, better hurry up and laugh before they disappear! 😄":
#         file.write("## Warning: The memes you see here are highly volatile and have a limited lifespan of 5 minutes. So, better hurry up and laugh before they disappear! 😄\n\n")
    file.write(markdown + "\n\n")
    file.writelines(contents)
# # Add a warning message at the beginning of the contents
# warning = "## Warning: The memes you see here are highly volatile and have a limited lifespan of 5 minutes. So, better hurry up and laugh before they disappear! 😄\n\n"
# contents.insert(0, warning)

# # Write the Markdown to the README.md file
# with open('README.md', 'w') as file:
#     file.writelines(contents)
#     file.write(markdown + "\n\n")
