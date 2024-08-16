from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests

# Configure Selenium to use a headless browser
chrome_options = Options()
chrome_options.add_argument("--headless")

# Set up the WebDriver (Make sure the correct path to your chromedriver is set)
driver = webdriver.Chrome(options=chrome_options)

# The URL you want to scrape
base_url = "https://www.asx.com.au/asx/1/company/{TICKER}/announcements?count=20&market_sensitive=false"

# Use Selenium to open the URL
driver.get(base_url)

time.sleep(30)  # Wait 30 seconds for CAPTCHA solving manually

# After the CAPTCHA is solved, Selenium has cookies that we can use in a requests session
cookies = driver.get_cookies()

list_of_tickers = ["AEE", "REZ", "1AE", "1MC", "NRZ"]

for ticker in list_of_tickers:
    
    # Convert cookies to a format requests can use
    session = requests.Session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    url = base_url.replace("{TICKER}", ticker)
    
    headers = {'Content-type': 'application/json'}
    
    response = session.get(url)

    if response.status_code == 200:
        announcements = response.json()

        print(f"Ticker: {ticker}")
        print(announcements)
    else:
        print(f"Failed to retrieve data for ticker: {ticker}")

print('Success')