import requests
from src.scraper.parser_updated import extract_us_market_prices

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_yahoo_home():
    response = requests.get(
        "https://finance.yahoo.com",
        headers=HEADERS,
        timeout=10
    )
    response.raise_for_status()

    return extract_us_market_prices(response.text)
