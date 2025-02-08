from dotenv import load_dotenv
import os

from data_sources import DataSources
from tweet_getter import TweetGetter

import asyncio

if __name__ == '__main__':
    load_dotenv()

    data_sources = DataSources('data/uganda_sources.json')
    twitter = TweetGetter()
    async def login():
        await twitter.login(os.environ['TWITTER_USERNAME'], os.environ['TWITTER_PASSWORD'], os.environ['COOKIES_PATH'])

    asyncio.run(login())

    async def main():
        username = "inakasiita1"
        tweets = await twitter.get_tweets_from_user(username)
        print(tweets)
        twitter.store_tweets_to_excel(tweets, f'data/{username}_tweets.xlsx')
        print("File saved")
        twitter.print_tweets(tweets)

    asyncio.run(main())