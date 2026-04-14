# Import the requests library to make HTTP requests
import requests
# Import the extract_us_market_prices function from the parser_updated module
from src.scraper.parser_updated import extract_us_market_prices

# Define a dictionary containing headers for the HTTP request, including a User-Agent to mimic a browser
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Define a function that scrapes market prices from Yahoo Finance's home page
def scrape_yahoo_home():
    # Make a GET request to the Yahoo Finance home page URL with the specified headers and a timeout of 10 seconds
    response = requests.get(
        "https://finance.yahoo.com",
        headers=HEADERS,
        timeout=10
    )
    # Raise an exception if the HTTP response indicates an error (e.g., 4xx or 5xx status codes)
    response.raise_for_status()

    # Return the result of extracting US market prices from the HTML text of the response
    return extract_us_market_prices(response.text)
