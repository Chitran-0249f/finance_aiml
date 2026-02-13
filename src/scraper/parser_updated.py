from bs4 import BeautifulSoup
import logging

def extract_us_market_prices(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    symbols = {
        "sp_futures": "ES=F",
        "dow_futures": "YM=F",
        "nasdaq_futures": "NQ=F",
        "gold": "GC=F",
        "crude_oil": "CL=F",
        "russell_2000": "RTY=F",
        "vix": "^VIX"
    }

    results = {}

    for column, symbol in symbols.items():
        tag = soup.find(
            "fin-streamer",
            {"data-symbol": symbol, "data-field": "regularMarketPrice"}
        )

        if not tag or tag.text.strip() == "":
            logging.warning(f"{column} missing")
            results[column] = None
            continue

        text = tag.text.strip()

        try:
            results[column] = float(text.replace(",", ""))
        except ValueError:
            logging.error(f"{column} invalid value: {text}")
            results[column] = None

    return results