import asyncio
from twikit import Client
import os
import random

class TweetGetter:
    """
    A class to interact with the Twitter API and get tweets.
    """
    def __init__(self):
        """
        Initialize the TweetGetter class.
        """
        self.client = Client('en-US')
        #self.client.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})


    async def login(self, username, email, password, cookies_path):
        """
        Login to Twitter if the session does not exist yet.
        
        If the session does not exist, the method will login to Twitter using the
        provided credentials and save the cookies to the specified path.
        
        If the session already exists, the method will load the cookies from the
        specified path.
        
        Parameters:
        username (str): The username to log in with
        email (str): The email address to log in with
        password (str): The password to log in with
        cookies_path (str): The path to save the cookies to
        """
        if not os.path.exists(cookies_path):
            # If the session does not exist, login and save the cookies
            await self.client.login(
                auth_info_1=username,
                auth_info_2=email,
                password=password
            )
            self.client.save_cookies(cookies_path)
        else:
            # If the session already exists, load the cookies
            print("Already logged in")
            self.client.load_cookies(cookies_path)

    async def get_tweets_from_user(self, username):
        """
        Get tweets from a user.
        
        This function will get tweets from a user with the specified username.
        
        Parameters:
        username (str): The username of the user to get tweets from
        
        Returns:
        list[dict]: A list of tweets from the user
        """
        # Get the user object
        user = await self.client.get_user_by_screen_name(username)

        await asyncio.sleep(random.uniform(2, 5))  # Random delay between 2-5 sec
        tweets = await user.get_tweets('Tweets', count=40)

        tweets_to_store = []

        for tweet in tweets:
            if tweet.retweeted_tweet:
                tweet = tweet.retweeted_tweet
            tweets_to_store.append({
                'id': tweet.id,
                'user': tweet.user.screen_name,
                'created_at': tweet.created_at,
                'favorite_count': tweet.favorite_count,
                'retweet_count': tweet.reply_count,
                'full_text': tweet.full_text,
                'lang': tweet.lang,
            })

        return tweets_to_store

#    def print_tweets(self, tweets_to_store):
#        #print(df.sort_values(by='favorite_count', ascending=False))
#        print(json.dumps(tweets_to_store, indent=4))