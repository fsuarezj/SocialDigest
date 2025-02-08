import asyncio
from twikit import Client
import json
import pandas as pd
import os

class TweetGetter:
    def __init__(self):
        self.client = Client('en-US')

    async def login(self, username, password, cookies_path):
        if not os.path.exists(cookies_path):
            await self.client.login(
                auth_info_1=username,
                password=password
            )

            self.client.save_cookies(cookies_path)
        else:
            self.client.load_cookies(cookies_path)

    async def get_tweets_from_user(self, username):
        user = await self.client.get_user_by_screen_name(username)

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

    def store_tweets_to_excel(self, tweets_to_store, file_name='tweets.xlsx'):
        df = pd.DataFrame(tweets_to_store)
        df.to_excel(file_name, index=False)
    
    def print_tweets(self, tweets_to_store):
        #print(df.sort_values(by='favorite_count', ascending=False))
        print(json.dumps(tweets_to_store, indent=4))