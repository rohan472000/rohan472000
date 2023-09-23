#  Copyright (c) 2023 Rohan Anand (anand00rohan@gmail.com), rohan472000 on GitHub
import requests
import json
import re

# Define the API endpoint to fetch memes
reddit_api_url = "https://www.reddit.com/r/memes/random.json?limit=1"

# Define a user agent to mimic a web browser
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)

def fetch_random_meme(api_url, user_agent):
    try:
        # Make a request to the Reddit API with the specified user agent
        response = requests.get(api_url, headers={'User-agent': user_agent})

        # Check if the request was successful
        if response.status_code == 200:
            meme_data = json.loads(response.text)
            return meme_data
        else:
            print(f"Failed to fetch meme. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred while fetching the meme: {str(e)}")
        return None

def extract_meme_url(meme_data):
    try:
        # Extract meme URL from the JSON response
        if (
            isinstance(meme_data, list)
            and len(meme_data) > 0
            and isinstance(meme_data[0], dict)
            and "data" in meme_data[0]
            and "children" in meme_data[0]["data"]
            and len(meme_data[0]["data"]["children"]) > 0
            and "data" in meme_data[0]["data"]["children"][0]
            and "url" in meme_data[0]["data"]["children"][0]["data"]
        ):
            meme_url = meme_data[0]["data"]["children"][0]["data"]["url"]
            return meme_url + "?width=100&height=100"  # Add query string to reduce image size
        else:
            print("Unexpected JSON structure in the response.")
            return None
    except Exception as e:
        print(f"An error occurred while extracting meme URL: {str(e)}")
        return None

def update_readme_with_meme(markdown):
    try:
        # Read the existing contents of README.md
        with open('README.md', 'r') as file:
            contents = file.readlines()

        # Remove any existing meme Markdowns from the contents
        contents = [line for line in contents if not re.match(r"!\[Funny Meme\]\(.*\)", line)]

        # Append the new meme Markdown to the README.md file
        with open('README.md', 'w') as file:
            file.write(markdown + "\n\n")
            file.writelines(contents)
    except Exception as e:
        print(f"An error occurred while updating README.md: {str(e)}")

def main():
    meme_data = fetch_random_meme(reddit_api_url, user_agent)
    if meme_data:
        meme_url = extract_meme_url(meme_data)
        if meme_url:
            # Create a Markdown image link with the meme URL
            markdown = f"![Funny Meme]({meme_url})"
            update_readme_with_meme(markdown)

if __name__ == "__main__":
    main()
