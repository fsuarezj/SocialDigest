from selenium import webdriver
# import undetected_chromedriver as uc 
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import os
import json
import time
import random
from datetime import datetime

MAX_TWEETS = 10
USER_AGENTS = [
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Version/17.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:115.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:115.0) Gecko/20100101 Firefox/115.0'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
]


class SeleniumDriver:
    def _get_headless_chrome_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
        chrome_options.add_argument("--disable-gpu")  # Recommended for headless mode
        chrome_options.add_argument("--window-size=1920x1080")  # Set window size
        chrome_options.add_argument("--ignore-certificate-errors")  # Ignore SSL issues

        driver = webdriver.Chrome(options=chrome_options)
        return driver
    
    def _get_undetected_chrome_driver(self):
        # create a ChromeOptions object
        options = webdriver.ChromeOptions()
        #run in headless mode
        options.add_argument("--headless")
        # disable the AutomationControlled feature of Blink rendering engine
        options.add_argument('--disable-blink-features=AutomationControlled')
        # disable pop-up blocking
        options.add_argument('--disable-popup-blocking')
        # start the browser window in maximized mode
        options.add_argument('--start-maximized')
        # disable extensions
        options.add_argument('--disable-extensions')
        # disable sandbox mode
        options.add_argument('--no-sandbox')
        # disable shared memory usage
        options.add_argument('--disable-dev-shm-usage')
        # choose random user agent
        options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')

        driver = webdriver.Chrome(options=options)
        # Change the property value of the navigator for webdriver to undefined
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def _change_user_agent(self, driver):
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": random.choice(USER_AGENTS)})

class RandomWait:
    def _random_wait(self, base_time):
        """Waits for a random time between (base_time - 1) and (base_time + 1) seconds"""
        wait_time = random.uniform(base_time - 1, base_time + 1)
        time.sleep(max(1, wait_time))  # Ensuring minimum 1 sec wait

class SeleniumHumanBehavior:
    def human_like_scroll(self, driver, min_scroll_ratio=0.05, max_scroll_ratio=0.15, min_delay=0.2, max_delay=0.5):
        """
        Scrolls down the page in small, random increments based on page height.

        :param driver: Selenium WebDriver instance
        :param min_scroll_ratio: Minimum percentage of page height to scroll per step
        :param max_scroll_ratio: Maximum percentage of page height to scroll per step
        :param min_delay: Minimum wait time between scrolls (seconds)
        :param max_delay: Maximum wait time between scrolls (seconds)
        """
        last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial page height
        total_scrolls = random.randint(5, 10)  # Random number of scrolls

        for _ in range(total_scrolls):
            step = random.randint(int(last_height * min_scroll_ratio), int(last_height * max_scroll_ratio))  # Dynamic step
            driver.execute_script(f"window.scrollBy(0, {step})")  # Scroll by calculated step
            time.sleep(random.uniform(min_delay, max_delay))  # Randomized delay

            # Update the page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # If the height hasn't changed significantly, break out (end of page)
            if new_height - last_height < 50:  # Adjust threshold if needed
                break
            
            last_height = new_height  # Update last height

        # Final small adjustment to reach bottom naturally
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
    

    def simulate_human_scroll(self, driver, min_scroll_ratio=0.05, max_scroll_ratio=0.15, min_delay=0.2, max_delay=0.5, mouse_move=True):
        """
        Scrolls down the page in a human-like way, with pauses and mouse movements.

        :param driver: Selenium WebDriver instance
        :param min_scroll_ratio: Min percentage of page height to scroll per step
        :param max_scroll_ratio: Max percentage of page height to scroll per step
        :param min_delay: Minimum wait time between scrolls (seconds)
        :param max_delay: Maximum wait time between scrolls (seconds)
        :param mouse_move: Whether to include human-like mouse movements
        """
        last_height = driver.execute_script("return document.body.scrollHeight")  # Get initial page height
        total_scrolls = random.randint(5, 10)  # Random number of scrolls
        action = ActionChains(driver)  # Initialize action chain for mouse movements

        for i in range(total_scrolls):
            step = random.randint(int(last_height * min_scroll_ratio), int(last_height * max_scroll_ratio))  # Dynamic step
            driver.execute_script(f"window.scrollBy(0, {step})")  # Scroll by calculated step
            time.sleep(random.uniform(min_delay, max_delay))  # Randomized delay

            # Simulate reading by randomly pausing
            if random.random() < 0.3:  # 30% chance of stopping
                pause_time = random.uniform(1, 4)  # Pause between 1-4 seconds
                print(f"Pausing for {pause_time:.2f} sec to simulate reading")
                time.sleep(pause_time)

            # Simulate mouse movement
            if mouse_move and random.random() < 0.5:  # 50% chance of mouse movement
                x_offset = random.randint(50, 400)
                y_offset = random.randint(50, 300)
                action.move_by_offset(x_offset, y_offset).perform()
                print(f"Mouse moved to ({x_offset}, {y_offset})")

            # Update the page height after scrolling
            new_height = driver.execute_script("return document.body.scrollHeight")

            # If the height hasn't changed significantly, break out (end of page)
            if new_height - last_height < 50:  # Adjust threshold if needed
                break
            
            last_height = new_height  # Update last height

        # Final small flick to the bottom
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")



class SeleniumScraper(RandomWait, SeleniumDriver, SeleniumHumanBehavior):
    """
    A class to scrape tweets from a user's profile using Selenium.
    Methods
    -------
    __init__():
        Initializes the SeleniumScraper with a headless Chrome driver.
    __del__():
        Closes the main driver when the instance is deleted.
    scrape_tweets(username, num_tweets):
        Scrapes a specified number of tweets from a user's profile.
    remove_duplicates():
        Removes duplicate tweets from the collected data.
    sort_tweets():
        Sorts the collected tweets by datetime in descending order.
    get_tweets():
        Returns the collected tweets data.
    get_error_tweets():
        Returns the collected error tweets data.
    _collect_tweet_from_div(tweet_text_div):
        Collects tweet data from a tweet text div element.
    _collect_tweet_from_page(username, tweet_id):
        Collects tweet data from an individual tweet page.
    _get_expanded_text(username, tweet_id):
        Gets the full text of a tweet that is truncated.
    _get_text_with_links(tweet_text_div):
        Extracts text, mentions, and hashtags from a tweet text div element.
    _expand_tweets(tweets):
        Expands truncated tweets to get their full text.
    _add_username_and_tweet_id_from_div(result, tweet_text_div):
        Adds the username and tweet ID to the result dictionary from a tweet text div element.
    _add_datetime_from_div(result, tweet_text_div):
        Adds the datetime of the tweet to the result dictionary from a tweet text div element.
    _is_retweet(tweet_text_div):
        Checks if a tweet is a retweet.
    """

    def __init__(self):
        """
        Initializes the SeleniumScraper with a headless Chrome driver.
        
        Args:
            None
        
        Attributes:
            main_driver (webdriver.Chrome): The main Chrome driver instance.
            tweets_data (list): A list of dictionaries containing tweet data.
            error_tweets_data (list): A list of dictionaries containing error tweet data.
        """
        #self.main_driver = webdriver.Chrome()
        # self.main_driver = self._get_headless_chrome_driver()
        self.main_driver = self._get_undetected_chrome_driver()

    def __del__(self):
        # Close driver
        """
        Closes the main driver when the instance is deleted.
        """
        self.main_driver.quit()

    def scrape_tweets(self, username, num_tweets = MAX_TWEETS):
        """
        Scrapes a specified number of tweets from a user's profile.

        Args:
            username (str): The username of the Twitter profile to scrape.
            num_tweets (int): The number of tweets to scrape.

        Returns:
            None
        """
        self.tweets_data = self.load_from_file(username)
        self.error_tweets_data = []
        self.tweeter_name = username
        self.main_driver.get(f"https://x.com/{self.tweeter_name}")

        # self.main_driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        self.simulate_human_scroll(self.main_driver)
        while len(self.tweets_data) < num_tweets:
            aux_tweets_data = []
            aux_errors_tweets_data = []
            self._random_wait(5)  # Random wait before next scroll
            tweet_text_divs = self.main_driver.find_elements(By.XPATH, '//div[@data-testid="tweetText"]')
            print(f"Found {len(tweet_text_divs)} tweets")
            for tweet_text_div in tweet_text_divs:
                try:
                    collected_tweet = self._collect_tweet_from_div(tweet_text_div)
                    if "error" not in collected_tweet:
                        aux_tweets_data.append(collected_tweet)
                    else:
                        aux_errors_tweets_data.append(collected_tweet)
                except Exception as e:
                    print(f"Error extracting tweet: {e.message}")

            # self.main_driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            self.simulate_human_scroll(self.main_driver)
            self._expand_tweets(aux_tweets_data)
            print(f"{len(aux_tweets_data)} tweets scraped | {len(aux_errors_tweets_data)} errors scraped")
            self.tweets_data = self.tweets_data + aux_tweets_data
            self.error_tweets_data = self.error_tweets_data + aux_errors_tweets_data
            print(f"Total tweets scrapped: {len(self.tweets_data)}")
        
        self.remove_duplicates()
        self.sort_tweets()
        print(f"Total tweets scrapped after deduplication: {len(self.tweets_data)}")
        self.save_to_file()

    def remove_duplicates(self):
        """
        Removes duplicate tweets from the collected data.
        
        After scraping tweets from a user's profile, some tweets may be scraped multiple times.
        This method removes these duplicates from the collected data.
        """
        
        self.tweets_data = {tweet['tweet_id']: tweet for tweet in self.tweets_data if isinstance(tweet, dict)}
        self.tweets_data = list(self.tweets_data.values())
        self.error_tweets_data = {tweet['tweet_text']: tweet for tweet in self.error_tweets_data if isinstance(tweet, dict)}
        self.error_tweets_data = list(self.error_tweets_data.values())
    
    def sort_tweets(self):
        """
        Sorts the collected tweets by datetime in descending order.

        This method sorts the tweets stored in `self.tweets_data` based on their
        `tweet_datetime` field, ensuring that the most recent tweets appear first.
        """

        self.tweets_data = sorted(self.tweets_data, key=lambda x: datetime.strptime(x['tweet_datetime'], '%Y-%m-%dT%H:%M:%S.%f%z'), reverse=True)

    def get_tweets(self):
        return self.tweets_data
    
    def get_error_tweets(self):
        return self.error_tweets_data
    
    def save_to_file(self, file_path=None):
        if not file_path:
            file_path = f"data/tweets/{self.tweeter_name}_tweets.json"
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        with open(file_path, 'w') as file:
            json.dump(self.tweets_data, file, indent=4)
    
    def load_from_file(self, username, file_path=None):
        if not file_path:
            file_path = f"data/tweets/{username}_tweets.json"
        try:
            with open(file_path, 'r') as file:
                tweets_data = json.load(file)
        except FileNotFoundError:
            tweets_data = []
            print(f"File {file_path} does not exist.")
        return tweets_data

    def _collect_tweet_from_div(self, tweet_text_div):
        result = {}
        is_retweet = False
        # Extract tweet text
        result["tweet_text"], mentions, hashtags = self._get_text_with_links(tweet_text_div)
        if mentions: result["mentions"] = mentions
        if hashtags: result["hashtags"] = hashtags

        is_retweet = self._is_retweet(tweet_text_div)
        
        try:
            tweet_text_div.find_element(By.XPATH, './ancestor::div[1]/div[@data-testid="tweet-text-show-more-link"]')
            result["to_expand"] = True  # If found, it means the tweet is truncated
        except:
            result["to_expand"] = False  # If not found, the tweet is fully visible

        self._add_username_and_tweet_id_from_div(result, tweet_text_div)
        if not is_retweet: self._add_datetime_from_div(result, tweet_text_div)

        if is_retweet:
            result = self._collect_tweet_from_page(result["username"], result["tweet_id"])

        return result

    def _collect_tweet_from_page(self, username, tweet_id):
        try:
            # Construct the tweet URL
            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
            print("Getting individual tweet for URL: ", tweet_url)

            # Open a new browser instance for each tweet
            # aux_driver = self._get_headless_chrome_driver()
            aux_driver = self._get_undetected_chrome_driver()
            aux_driver.get(tweet_url)

            self._random_wait(3)  # Random wait before next scroll

            # Get the full tweet text
            tweet_text_div = aux_driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]')
            result = {}
            result["tweet_text"], mentions, hashtags = self._get_text_with_links(tweet_text_div)
            if mentions: result["mentions"] = mentions
            if hashtags: result["hashtags"] = hashtags
            result["to_expand"] = False
            result["username"] = username
            result["tweet_id"] = tweet_id

            try:
                tweet_container = tweet_text_div.find_element(By.XPATH, "./ancestor::div[3]")
                self._add_datetime_from_div(result, tweet_container)
            except:
                result["error"] = "Error finding tweet datetime"

            # Close the temporary driver
            aux_driver.quit()
        except Exception as e:
            print(f"Error going to retweet {tweet['tweet_id']}: {e}")
            aux_driver.quit()
            raise(e)
        return result

    def _get_expanded_text(self, username, tweet_id):
        try:
            # Construct the tweet URL
            tweet_url = f"https://x.com/{username}/status/{tweet_id}"
            print("Getting text of the tweet for URL: ", tweet_url)

            # Open a new browser instance for each tweet
            # aux_driver = self._get_headless_chrome_driver()
            aux_driver = self._get_undetected_chrome_driver()
            aux_driver.get(tweet_url)

            self._random_wait(3)  # Random wait before next scroll

            # Get the full tweet text
            tweet_text = aux_driver.find_element(By.XPATH, '//div[@data-testid="tweetText"]').text

            # Close the temporary driver
            aux_driver.quit()
        except Exception as e:
            print("EEEEEEEEEEEEEEERRRRRRRRRRRRRROOOOOOOOOOOOOOOORRRRRRRRRRRRRRRR")
            print(f"Error expanding tweet {tweet['tweet_id']}: {e}")
            aux_driver.quit()
            raise(e)
        return tweet_text
    
    def _get_text_with_links(self, tweet_text_div):
            text = tweet_text_div.text
            links = []
            mentions = []
            hashtags = []
            try:
                links = tweet_text_div.find_elements(By.XPATH, './/a')
            except:
                pass
            for link in links:
                old_link = link.text
                if old_link[0] == "@":
                    mentions.append(old_link)
                elif old_link[0] == "#":
                    hashtags.append(old_link)
                else: 
                    new_link = link.get_attribute("href")
                    text = text.replace(old_link, new_link)
            return text, mentions, hashtags

    def _expand_tweets(self, tweets):
        for tweet in tweets:
            if tweet["to_expand"]:
                expanded_text = self._get_expanded_text(tweet["username"], tweet["tweet_id"])
                tweet["tweet_text"] = expanded_text
                tweet["to_expand"] = False

    def _add_username_and_tweet_id_from_div(self, result, tweet_text_div):
        try:
            # Find the User-Name div
            user_name_div = tweet_text_div.find_element(By.XPATH, "./ancestor::div[2]/div[1]")
        except:
            result["error"] = "Error finding user name div"

        # Find the <a> inside it to get username and tweet ID
        try:
            user_link = user_name_div.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
            tweet_url = user_link.get_attribute("href")
            # Extract username and tweet ID from the URL
            result["username"], result["tweet_id"] = tweet_url.split("/")[-3], tweet_url.split("/")[-1]
        except:
            result["error"] = "Error finding user link"

    def _add_datetime_from_div(self, result, tweet_text_div):
        try:
            # Find the <time> element inside the tweet container and get its datetime value
            time_element = tweet_text_div.find_element(By.XPATH, "./ancestor::div[2]//time")
            result["tweet_datetime"] = time_element.get_attribute("datetime")
        except:
            result["error"] = "Error finding tweet datetime"

    def _is_retweet(self, tweet_text_div):
        try:
            context = tweet_text_div.find_element(By.XPATH, "./ancestor::div[4]/div[1]").text
            return context and context[-8:] == "reposted"
        except:
            return False
