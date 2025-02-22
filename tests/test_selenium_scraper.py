import pytest
from unittest.mock import patch, MagicMock
from selenium_scraper import SeleniumScraper, MAX_TWEETS

@pytest.fixture
def scraper():
    with patch('selenium_scraper.SeleniumDriver._get_headless_chrome_driver') as mock_driver:
        mock_driver.return_value = MagicMock()
        return SeleniumScraper()

def test_scrape_tweets(scraper):
    scraper.main_driver.get = MagicMock()
    scraper.main_driver.execute_script = MagicMock()
    scraper.main_driver.find_elements = MagicMock(return_value=[MagicMock() for _ in range(MAX_TWEETS)])
    scraper._collect_tweet_from_div = MagicMock(return_value={"tweet_id": "123", "tweet_text": "Test tweet", "tweet_datetime": "2023-01-01T00:00:00.000Z"})
    scraper._expand_tweets = MagicMock()

    scraper.scrape_tweets("testuser", MAX_TWEETS)

    assert len(scraper.get_tweets()) == MAX_TWEETS
    assert scraper.main_driver.get.called
    assert scraper.main_driver.execute_script.called
    assert scraper._collect_tweet_from_div.called
    assert scraper._expand_tweets.called

def test_remove_duplicates(scraper):
    scraper.tweets_data = [
        {"tweet_id": "123", "tweet_text": "Test tweet 1"},
        {"tweet_id": "123", "tweet_text": "Test tweet 1"},
        {"tweet_id": "456", "tweet_text": "Test tweet 2"}
    ]
    scraper.remove_duplicates()
    assert len(scraper.get_tweets()) == 2

def test_sort_tweets(scraper):
    scraper.tweets_data = [
        {"tweet_id": "123", "tweet_text": "Test tweet 1", "tweet_datetime": "2023-01-01T00:00:00.000Z"},
        {"tweet_id": "456", "tweet_text": "Test tweet 2", "tweet_datetime": "2023-01-02T00:00:00.000Z"}
    ]
    scraper.sort_tweets()
    assert scraper.get_tweets()[0]["tweet_id"] == "456"

def test_collect_tweet_from_div(scraper):
    tweet_div = MagicMock()
    tweet_div.text = "Test tweet"
    scraper._get_text_with_links = MagicMock(return_value=("Test tweet", [], []))
    scraper._is_retweet = MagicMock(return_value=False)
    scraper._add_username_and_tweet_id_from_div = MagicMock()
    scraper._add_datetime_from_div = MagicMock()

    tweet = scraper._collect_tweet_from_div(tweet_div)
    assert tweet["tweet_text"] == "Test tweet"
    assert "error" not in tweet

def test_collect_tweet_from_page(scraper):
    scraper._get_headless_chrome_driver = MagicMock(return_value=MagicMock())
    scraper._get_text_with_links = MagicMock(return_value=("Test tweet", [], []))
    scraper._add_datetime_from_div = MagicMock()

    tweet = scraper._collect_tweet_from_page("testuser", "123")
    assert tweet["tweet_text"] == "Test tweet"
    assert tweet["username"] == "testuser"
    assert tweet["tweet_id"] == "123"

def test_expand_tweets(scraper):
    scraper._get_expanded_text = MagicMock(return_value="Expanded tweet text")
    tweets = [{"username": "testuser", "tweet_id": "123", "tweet_text": "Test tweet", "to_expand": True}]
    scraper._expand_tweets(tweets)
    assert tweets[0]["tweet_text"] == "Expanded tweet text"
    assert not tweets[0]["to_expand"]

def test_get_tweets(scraper):
    scraper.tweets_data = [
        {"tweet_id": "123", "tweet_text": "Test tweet 1"},
        {"tweet_id": "456", "tweet_text": "Test tweet 2"}
    ]
    tweets = scraper.get_tweets()
    assert len(tweets) == 2
    assert tweets[0]["tweet_id"] == "123"
    assert tweets[1]["tweet_id"] == "456"

def test_get_error_tweets(scraper):
    scraper.error_tweets_data = [
        {"tweet_id": "789", "tweet_text": "Error tweet 1"},
        {"tweet_id": "101", "tweet_text": "Error tweet 2"}
    ]
    error_tweets = scraper.get_error_tweets()
    assert len(error_tweets) == 2
    assert error_tweets[0]["tweet_id"] == "789"
    assert error_tweets[1]["tweet_id"] == "101"

def test_add_username_and_tweet_id_from_div(scraper):
    tweet_div = MagicMock()
    user_link = MagicMock()
    user_link.get_attribute = MagicMock(return_value="https://x.com/testuser/status/123")
    tweet_div.find_element = MagicMock(return_value=user_link)
    result = {}
    scraper._add_username_and_tweet_id_from_div(result, tweet_div)
    assert result["username"] == "testuser"
    assert result["tweet_id"] == "123"

def test_add_datetime_from_div(scraper):
    tweet_div = MagicMock()
    time_element = MagicMock()
    time_element.get_attribute = MagicMock(return_value="2023-01-01T00:00:00.000Z")
    tweet_div.find_element = MagicMock(return_value=time_element)
    result = {}
    scraper._add_datetime_from_div(result, tweet_div)
    assert result["tweet_datetime"] == "2023-01-01T00:00:00.000Z"

def test_is_retweet(scraper):
    tweet_div = MagicMock()
    context_div = MagicMock()
    context_div.text = "testuser reposted"
    tweet_div.find_element = MagicMock(return_value=context_div)
    is_retweet = scraper._is_retweet(tweet_div)
    assert is_retweet

def test_is_not_retweet(scraper):
    tweet_div = MagicMock()
    context_div = MagicMock()
    context_div.text = "testuser tweeted"
    tweet_div.find_element = MagicMock(return_value=context_div)
    is_retweet = scraper._is_retweet(tweet_div)
    assert not is_retweet