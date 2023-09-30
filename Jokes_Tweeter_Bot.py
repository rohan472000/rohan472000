import tweepy
import joke

# Define the API endpoint to fetch memes
reddit_api_url = "https://www.reddit.com/r/memes/random.json?limit=1"

# Define a user agent to mimic a web browser
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
)

meme_data = joke.fetch_random_meme(reddit_api_url, user_agent)
meme_url = joke.extract_meme_url(meme_data)

# print(meme_url)

# Twitter (X) developer credentials 
# Get these from twitter(X) developer's account
 
api_key = ""
api_secret = ""
bearer_token = r""
access_token = ""
access_token_secret = ""

client = tweepy.Client(bearer_token,api_key,api_secret,access_token,access_token_secret)
auth = tweepy.OAuth1UserHandler(api_key,api_secret,access_token,access_token_secret)
api = tweepy.API(auth)

client.create_tweet(text=f"{meme_url} \n#Memes #Jokes #Reddit") 
