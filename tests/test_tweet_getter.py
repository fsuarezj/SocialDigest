import pytest
from pytest_mock import MockerFixture
from tweet_getter import TweetGetter
import asyncio
from unittest.mock import AsyncMock, MagicMock

@pytest.fixture
def tweet_getter(mocker: MockerFixture):
    mocker.patch('tweet_getter.Client')
    yield TweetGetter()

@pytest.mark.asyncio
async def test_login_new_user(tweet_getter, mocker: MockerFixture):
    mock_login = mocker.patch.object(tweet_getter.client, 'login')
    mock_login = AsyncMock()
    mock_save_cookies = mocker.patch.object(tweet_getter.client, 'save_cookies')
    mock_save_cookies = MagicMock()
    await tweet_getter.login('username', 'email', 'password', 'cookies_path')
    mock_login.assert_awaited_once_with(auth_info_1='username', auth_info_2='email', password='password', cookies_file='cookies_path')
    mock_save_cookies.assert_called_once_with('cookies_path')

def test_login_existing_user(tweet_getter, mocker: MockerFixture):
    mock_path_exists = mocker.patch('os.path.exists', return_value=True)
    mock_client_load_cookies = mocker.patch.object(TweetGetter, 'main_client').load_cookies
    asyncio.run(tweet_getter.login('username', 'email', 'password', 'cookies_path'))
    mock_client_load_cookies.assert_called_once_with('cookies_path')

async def test_get_tweets_from_user(tweet_getter, mocker: MockerFixture):
    mock_get_user_by_screen_name = mocker.patch.object(TweetGetter, 'client').get_user_by_screen_name
    mock_get_user_by_screen_name = AsyncMock()
    mock_get_tweets = mocker.patch.object(TweetGetter, 'client').get_user_by_screen_name().get_tweets
    mock_get_tweets = pytest.AsyncMock()
    mock_tweet = pytest.MagicMock()
    mock_tweet.retweeted_tweet = None
    mock_tweet.id = '123'
    mock_tweet.user.screen_name = 'user'
    mock_tweet.created_at = '2023-01-01'
    mock_tweet.favorite_count = 10
    mock_tweet.reply_count = 5
    mock_tweet.full_text = 'This is a tweet'
    mock_tweet.lang = 'en'
    mock_get_tweets.return_value = [mock_tweet]

    tweets = await tweet_getter.get_tweets_from_user('username')
    assert len(tweets) == 1
    assert tweets[0]['id'] == '123'
    assert tweets[0]['user'] == 'user'
    assert tweets[0]['created_at'] == '2023-01-01'
    assert tweets[0]['favorite_count'] == 10
    assert tweets[0]['retweet_count'] == 5
    assert tweets[0]['full_text'] == 'This is a tweet'
    assert tweets[0]['lang'] == 'en'
