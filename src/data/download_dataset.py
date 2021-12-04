from re import sub
from dotenv import find_dotenv, load_dotenv
import logging
import os
import pandas as pd
import praw
import re
import requests
import time
import urllib


def main():
    """ Main Function. """
    
    reddit = praw.Reddit(client_id=os.environ.get("client_id"),
                         client_secret=os.environ.get("client_secret"),
                         username=os.environ.get("username"),
                         password=os.environ.get("password"),
                         user_agent=os.environ.get("user_agent"))
    
    # Subreddits to scrape
    subreddits_list = ["architecture", "AbandonedPorn", "EarthPorn", "OldSchoolCool", "RoastMe", "SoccerPics"]
    
    # List of dataframes that will be concatenated
    dfs = []
    
    for subreddit_name in subreddits_list:

        # Initialize subreddit object
        subreddit = reddit.subreddit(subreddit_name)

        # list to hold rows of scraped data
        scraped_posts = []

        # Counts the number of posts scraped 
        count = 0

        # Specify number of text-image pairs to scrape per subreddit 
        num_to_scrape = 1000

        for post in subreddit.hot(limit=None):

            try:
                # Get post data
                post_id = str(post.id)
                post_author = str(post.author)
                post_text = str(post.title)
                url = str(post.url)
            except:
                continue    # skip this post

            # Check if post has both an image and some text and if so, append it
            if (len(post_text) > 0) and (url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png")):
                
                # Try downloading the image
                try:
                    # Retrieve the image and save it in current folder
                    urllib.request.urlretrieve(url, f"../../data/raw/images/{post_id}.png")
                except:
                    continue    # skip this post

                # Add row of data into dataframe
                scraped_posts.append([post_id, post_author, post_text, url])
                count += 1
            
            # If we've scraped what we needed
            if count >= num_to_scrape:
                
                # Convert list to pandas dataframe
                subreddit_df = pd.DataFrame(scraped_posts, columns=["id", "author", "text", "image_url"])

                # Specify label for dataframe (aka the subreddit)
                subreddit_df["subreddit_name"] = subreddit_name

                # Append to list of dataframes
                dfs.append(subreddit_df)

                # Break out of this subreddit
                break

            if count % 60 == 0 and count != 0:
                time.sleep(60)

    
    df = pd.concat(dfs, ignore_index=True)

    df.to_csv("../../data/raw/all-reddit-data.csv", index=False)

    print(df)


if __name__ == "__main__":

    # Initialize logging objects
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    for logger_name in ("praw", "prawcore"):
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()