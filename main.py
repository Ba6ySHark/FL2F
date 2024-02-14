import os
import time

# Library for sending requests to the API's endpoints
import requests

# Library for saving the data to .csv files
import pandas

# Library for loading the env variables from .env file
from dotenv import load_dotenv

# Loads variables from .env file
# Since the repository is public, I wanted to hide my Reddit credentials so that nobody steals my account
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
USERNAME = os.getenv("REDDIT_USERNAME")
PASSWORD = os.getenv("REDDIT_PASSWORD")

auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

# My Reddit account data that will be used for auth
data = {
    "grant_type": "password",
    "username": USERNAME,
    "password": PASSWORD
}

# Basic headers file that is sent in HTTP request
headers = {
    "User-Agent": "myapi/v1"
}

# Get the token for Reddit API via post method
TOKEN = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers).json()["access_token"]
# Update the headers to include authorization token
headers["Authorization"] = f"bearer {TOKEN}"

# I decided to create 2 pandas data frames

# The generic one carries all the results that were parsed
generic_data_frame = pandas.DataFrame()

# The tech one stores only the results that relate to AI, ML or technology (results should have any of these words in title)
tech_data_frame = pandas.DataFrame()

# Stores the id of the last seen post, so that we only check each post once
last_viewed_post = ""

#  The free version of Reddit API only allows users to send not more than 100 requests per minute
#  Therefore, I have included a time.sleep(60) statement at the end of the loop
#  The loop will run 10 times, which will result in 10*100 = 1000 results 
for i in range(15):
    # GET request to Reddit API that asks for the newest 100 posts after the latest_viewed_post
    res = requests.get("https://oauth.reddit.com/r/Entrepreneur/new", headers=headers, params={"limit": "100", "after": last_viewed_post})
    post_id = ""

    # For each of the 100 posts we get from the GET request above
    for post in res.json()["data"]["children"]:
        # Full id of the current post
        post_id = post["kind"] + "_" + post["data"]["id"]

        # Add the current post to the generic_data_frame
        generic_data_frame = generic_data_frame._append({
            "subreddit": post["data"]["subreddit"],
            "title": post["data"]["title"],
            "selftext": post["data"]["selftext"],
            "link": "https://www.reddit.com" + post["data"]["permalink"],
            "upvotes": post["data"]["ups"],
            "downvotes": post["data"]["downs"],
            "votes_ratio": post["data"]["upvote_ratio"]
        }, ignore_index=True)

        # If title includes technology, AI or ML -> add current post to tech_data_frame
        title = post["data"]["title"]
        if ("technology" in title) or ("AI" in title) or ("ML" in title):
            tech_data_frame = tech_data_frame._append({
            "subreddit": post["data"]["subreddit"],
            "title": post["data"]["title"],
            "selftext": post["data"]["selftext"],
            "link": "https://www.reddit.com" + post["data"]["permalink"],
            "upvotes": post["data"]["ups"],
            "downvotes": post["data"]["downs"],
            "votes_ratio": post["data"]["upvote_ratio"]
        }, ignore_index=True)
    
    print(f"Iteration {i+1} complete")
    last_viewed_post = post_id

    if i != 14:
        time.sleep(60)

# Convert the pandas data frames into csv files that can be viewed in Excel
generic_data_frame.to_csv("generic_data.csv")
tech_data_frame.to_csv("tech_data.csv")

print("Saved output as generic_data.csv and tech_data.csv")