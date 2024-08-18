# ASX Company Announcements

This project is created in order to collect and process a number of the latest announcements from ASX website base_url.
Currently, when accessing the base_url, CAPTCHA is triggered, therefore, to bypass it, API token should be requested from https://www.asxonline.com/mia/a/auth_token. Token could not be requested, instead, 2 ways of bypassing of the CAPTCHA were implemented that work locally:
- in announcements.py cookies, obtained after resolving CAPTCHA manually, were hardcoded;
- in streamlit_app.py similar approach has been used, but with the use of Selenium (resolving CAPTCHA still requires a manual action).

Due to the nature of manual resolution of CAPTCHA, when deploying the app to Streamlit, the app is failing with error due to manual action not being performed. It was decided to run streamlit locally and screen capture the results (the video is added: streamlit ran locally.mp4).

In order to verify that the application is runnable, 
- the Network URL can be provided when application is running locally
OR
- the ASX token can be provided in order to access API directly.
