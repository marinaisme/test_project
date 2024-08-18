from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import requests
import streamlit as st

base_url = "https://www.asx.com.au/asx/1/company/{TICKER}/announcements?count=20&market_sensitive=false"

cookies = {
    'JSESSIONID': '.node204',
    'TS019c39fc': '01856a822a60076d929638a9a634129f02d95fbb3c19b4837e70faa208a21ab412aaaa2fd00cc833ce8a24a592d25141fac7e6bca0',
    'affinity': '"50cd1fa853859882"',
    'incap_ses_276_2835827': '/6gTSIJYCFFC67ObrIzUA3IcwmYAAAAArqZZWlRPMu9ry45rtu5Q9A==',
    'nlbi_2835827': '/Mf+JMHdYExIGZQj2S5TNgAAAAA4uzR1RQvwmvXeNFXYAJUA',
    'nlbi_2835827_2708396': 'dMcQeLDaTli4vwQc2S5TNgAAAACDBsWUlHh8ZQP3rcBVst3s',
    'visid_incap_2835827': 'YEktWc8zSeKaw/mUp2VPPY/4wWYAAAAAQkIPAAAAAACAz262AU5JrHeXR9PxZMC2+4EtIMBHAorA'
}

list_of_tickers = ["AEE", "REZ", "1AE", "1MC", "NRZ"]
tickers_with_trading_halts = []

# Layout
st.title("ASX Company Announcements")

# Go through the list of tickers in order to find ones with "Trading Halt" announcements 
# and to add them to tickers_with_trading_halts list
for ticker in list_of_tickers:
    url = base_url.replace("{TICKER}", ticker)
    response = requests.get(url, cookies = cookies)

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
    response = requests.get(url, cookies = cookies)
    
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