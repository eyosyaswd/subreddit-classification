from pmaw import PushshiftAPI
from dotenv import find_dotenv, load_dotenv
import datetime as dt
import logging
import pandas as pd
import time
import urllib


def main():
    """ Main Function. """

    # Initialize Pushshift API object and date range for scraping data
    api = PushshiftAPI()

    # Subreddits to scrape
    subreddits_list = ["architecture", "AbandonedPorn", "EarthPorn", "OldSchoolCool", "RoastMe", "SoccerPics"]
    
    # List of rows of scraped data
    scraped_posts = []

    # Iterate through subreddits
    for subreddit_name in subreddits_list:

        start_time = time.time()

        # Get data generator for subreddit data
        posts = api.search_submissions(subreddit=subreddit_name, limit=5000)

        # Initialize counter for the number of posts scraped 
        count = 0

        for post in posts:
            # Get post data
            post_id = str(post["id"])
            post_author = str(post["author"])
            post_text = str(post["title"])
            url = str(post["url"])

            # Check if post has both an image and some text and if so, append it
            if (len(post_text) > 0) and (url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png")):
                
                # Try downloading the image
                try:
                    # Retrieve the image and save it in current folder
                    urllib.request.urlretrieve(url, f"../../data/raw/images/{post_id}.png")
                except:
                    # print("Error occurred when saving image.")
                    continue    # skip this post

                # Add row of data into dataframe
                scraped_posts.append([post_id, post_author, post_text, url, subreddit_name])
                count += 1
                # print(f"Count = {count}, Subreddit = {subreddit_name}")

                # Convert list to pandas dataframe
                df = pd.DataFrame(scraped_posts, columns=["id", "author", "text", "image_url", "subreddit_name"])

                # Output scraped data
                df.to_csv(data_filepath, index=False)
            
                # If we've scraped what we needed
                if count >= posts_per_subreddit:
                    
                    end_time = time.time() - start_time
                    print(f"\nScraped {count} posts from r/{subreddit_name} in {end_time} seconds. Breaking out of current subreddit.")

                    # Break out of this subreddit
                    break


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

    # Specify parameters
    data_filepath = "../../data/raw/all-reddit-data.csv"
    posts_per_subreddit = 1000    # Specify number of text-image pairs to scrape per subreddit 

    main()