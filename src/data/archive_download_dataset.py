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
    subreddits_list = ["EarthPorn", "OldSchoolCool", "RoastMe", "SoccerPics", "architecture", "AbandonedPorn"]
    
    # List of rows of scraped data
    scraped_posts = []
    
    for subreddit_name in subreddits_list:

        # Initialize subreddit object
        subreddit = reddit.subreddit(subreddit_name)

        # Counts the number of posts scraped 
        count = 0

        # Specify number of text-image pairs to scrape per subreddit 
        num_to_scrape = 1000

        for post in subreddit.new(limit=None):

            try:
                # Get post data
                post_id = str(post.id)
                post_author = str(post.author)
                post_text = str(post.title)
                url = str(post.url)
            except:
                print("Error occurred when reading in post data.")
                continue    # skip this post

            # Check if post has both an image and some text and if so, append it
            if (len(post_text) > 0) and (url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png")):
                
                # Try downloading the image
                try:
                    # Retrieve the image and save it in current folder
                    urllib.request.urlretrieve(url, f"../../data/raw/images/{post_id}.png")

                    # Add row of data into dataframe
                    scraped_posts.append([post_id, post_author, post_text, url, subreddit_name])
                    count += 1
                    print(f"Count = {count}, Subreddit = {subreddit_name}")

                    # Convert list to pandas dataframe
                    df = pd.DataFrame(scraped_posts, columns=["id", "author", "text", "image_url", "subreddit_name"])

                    # Output scraped data
                    df.to_csv("../../data/raw/all-new-reddit-data.csv", index=False)
                except:
                    print("Error likely occurred when saving image.")
                    continue    # skip this post
            
            # time.sleep(1)
            
            # If we've scraped what we needed
            if count >= num_to_scrape:
                
                # Convert list to pandas dataframe
                df = pd.DataFrame(scraped_posts, columns=["id", "author", "text", "image_url", "subreddit_name"])

                # Output scraped data
                df.to_csv("../../data/raw/all-new-reddit-data.csv", index=False)

                print(f"\nFinished with subreddit. Scraped {count} posts from r/{subreddit_name}. Breaking out of current subreddit.")

                # Break out of this subreddit
                break

            # # When we reach an API limit (60 calls per minute), sleep for a minute
            # if count % 30 == 0 and count != 0:    # to not hit the rate limit
                
            #     # Convert list to pandas dataframe
            #     df = pd.DataFrame(scraped_posts, columns=["id", "author", "text", "image_url", "subreddit_name"])

            #     # Output scraped data
            #     df.to_csv("../../data/raw/all-new-reddit-data.csv", index=False)

            #     print(f"\nScraped {count} posts from r/{subreddit_name}")
                
            #     # print("Sleeping for 5 seconds...")
            #     # time.sleep(5)
        # print(f"Count = {count}")
        # print(f"Num to Scrape = {num_to_scrape}")

    df.to_csv("../../data/raw/all-new-reddit-data.csv", index=False)

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