from dotenv import load_dotenv
#import os

from data_sources import DataSources
#from tweet_getter import TweetGetter, EmailManager
#from tweets_store import TweetsStore
from openvpn_manager import OpenVPNManager
from selenium_scraper import SeleniumScraper
import random

MAX_TWEETS = 20

import asyncio

async def login(tweet_getter):
    await tweet_getter.login(os.environ['TWITTER_USERNAME'],
                        os.getenv('TWITTER_EMAIL'),
                        os.environ['TWITTER_PASSWORD'],
                        os.environ['COOKIES_PATH']
    )

async def main(tweet_getter, username, store):
    print(f"Getting tweets from {username}")
    tweets = await tweet_getter.get_tweets_from_user(username)
    print(f"Got {len(tweets)} tweets from {username}")
    store.store_tweets(tweets)

async def get_all_tweets(tweet_getter, store):
    for username in data_sources.get_all_data_sources():
        await main(tweet_getter, username, store)

if __name__ == '__main__':
    load_dotenv()

    data_sources = DataSources('data/uganda_sources_all.json')
    # users = DataSources('data/user_accounts.json')
    # twitter = TweetGetter()
    # store = TweetsStore('data/uganda_tweets.xlsx')
    # email_manager = EmailManager()

    twitter_accounts = data_sources.get_all_sources_key("twitter_account")
    print(twitter_accounts)

    countries = ["fr", "ke", "nl", "uk", "ng", "za"]

    vpn_manager = OpenVPNManager()
    for twitter_account in twitter_accounts:
        try:
            country = random.choice(countries)
            vpn_manager.reconnect(country)  # Connect to a random server in the Netherlands
            scraper = SeleniumScraper()
            print(f"Scraping tweets from {twitter_account}")
            scraper.scrape_tweets(twitter_account, MAX_TWEETS)
        except Exception as e:
            print(f"Error scraping tweets from {twitter_account} from {country}: {e}")

    vpn_manager.disconnect()

    # Print extracted tweets
    #for tweet in scraper.get_tweets():
    #    print(tweet)

    # Example usage:
    #vpn_manager.status()
    #vpn_manager.reconnect("uk")  # Reconnect to the USA
    #vpn_manager.status()
    #created_users = users.filter_data_sources({"created": True})

    #print(len(created_users))
    #email_manager.create_email_address(user['email_address'], user['email_password'], 50)
    #asyncio.run(login(twitter))
    #asyncio.run(get_all_tweets(twitter, store))
