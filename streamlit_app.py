from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import requests
import streamlit as st

base_url = "https://www.asx.com.au/asx/1/company/{TICKER}/announcements?count=20&market_sensitive=false"

# Selenium is used to bypass CAPTCHA
chrome_options = Options()
chrome_options.add_argument("--headless")

# service = Service(ChromeDriverManager().install())
driver = uc.Chrome(options=chrome_options)
driver.get(base_url)

time.sleep(30)  # Wait for CAPTCHA to be solved manually

cookies = driver.get_cookies()
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

list_of_tickers = ["AEE", "REZ", "1AE", "1MC", "NRZ"]
tickers_with_trading_halts = []

# Layout
st.title("ASX Company Announcements")

# Go through the list of tickers in order to find ones with "Trading Halt" announcements 
# and to add them to tickers_with_trading_halts list
for ticker in list_of_tickers:
    url = base_url.replace("{TICKER}", ticker)
    response = session.get(url)

    if response.status_code == 200:
        data = response.json()

        # Check if 'data' key is present in the response
        if 'data' in data:
            announcements = data['data']
            # Filter "Trading Halt" announcements
            trading_halt_announcements = [ann for ann in announcements if "Trading Halt" in ann['header']]
            if trading_halt_announcements:
                tickers_with_trading_halts.append(ticker)

# Display tickers with "Trading Halt" announcements as a list in a separate section
if tickers_with_trading_halts:
    st.write("The following tickers have 'Trading Halt' announcements:")
    for ticker in tickers_with_trading_halts:
        st.write(f"- {ticker}")
else:
    st.write("There are no 'Trading Halt' announcements for the tickers.")

# Select a ticker using a sidebar drop-down menu
st.sidebar.header("Select a Ticker Symbol")
select_ticker = st.sidebar.selectbox("Select a Ticker Symbol", list_of_tickers)

# Display all the announcements for the selected ticker
if select_ticker:
    url = base_url.replace("{TICKER}", select_ticker)
    response = session.get(url)
    
    if response.status_code == 200:
        data = response.json()
    
        # Check if 'data' key is present in the response
        if 'data' in data:
            announcements = data['data']
            st.subheader(f"Announcements for {select_ticker}")
            
            # Filter "Trading Halt" announcements for the selected ticker
            show_trading_halt = st.button("Show Only 'Trading Halt' Announcements")
            
            if show_trading_halt:
                trading_halt_announcements = [ann for ann in announcements if "Trading Halt" in ann['header']]
                # Display only 'Trading Halt' announcements if the button is pressed
                if trading_halt_announcements:
                    st.write(f"Trading Halt Announcements for {select_ticker}:")
                    for ann in trading_halt_announcements:
                        st.write(ann)
                else:
                    st.write(f"No 'Trading Halt' announcements found for {select_ticker}.")
            else:
                # Display all announcements if the button is not pressed
                st.write("All announcements:")
                for ann in announcements:
                    st.write(ann)
        else:
            st.write("Unexpected response: No 'data' key found.")
    else:
        st.write(f"Failed to get data for ticker: {select_ticker}")

driver.quit()