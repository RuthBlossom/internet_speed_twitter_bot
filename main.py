from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Constants for promised internet speeds
PROMISED_DOWN = 150
PROMISED_UP = 10

# Path to ChromeDriver executable
CHROME_DRIVER_PATH = "C:\\chromedriver.exe"  # double backslashes for Windows file path

# Twitter credentials
TWITTER_EMAIL = "YOUR_TWITTER_EMAIL"
TWITTER_PASSWORD = "YOUR_TWITTER_PASSWORD"

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.driver = webdriver.Chrome(executable_path=driver_path)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net/")
        # Wait for the page to load
        time.sleep(5)

        # Click on the 'Go' button to start the speed test
        go_button = self.driver.find_element_by_css_selector(".start-button a")
        go_button.click()

        # Wait for the speed test to complete (adjust this time according to your internet speed)
        time.sleep(60)

        # Extract download and upload speeds from the page
        self.down = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text
        self.up = self.driver.find_element_by_xpath('//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text

    def tweet_at_provider(self):
        # Open Twitter login page
        self.driver.get("https://twitter.com/login")
        time.sleep(2)

        # Find email and password fields, and fill in the credentials
        email = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[1]/label/div/div[2]/div/input')
        password = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/form/div/div[2]/label/div/div[2]/div/input')
        email.send_keys(TWITTER_EMAIL)
        password.send_keys(TWITTER_PASSWORD)

        # Submit login credentials
        password.send_keys(Keys.ENTER)
        time.sleep(5)

        # Compose the tweet with speed information
        tweet_compose = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        tweet = f"Hey Internet Provider, why is my internet speed {self.down} down/{self.up} up when I pay for {PROMISED_DOWN} down/{PROMISED_UP} up?"
        tweet_compose.send_keys(tweet)
        time.sleep(3)

        # Click the tweet button to post the tweet
        tweet_button = self.driver.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_button.click()
        time.sleep(2)

        # Close the browser after posting the tweet
        self.driver.quit()

# Instantiate the bot and execute its functions
bot = InternetSpeedTwitterBot(CHROME_DRIVER_PATH)
bot.get_internet_speed()
bot.tweet_at_provider()

