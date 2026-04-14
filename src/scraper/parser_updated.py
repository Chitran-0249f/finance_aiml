# Import BeautifulSoup library for parsing HTML content
from bs4 import BeautifulSoup
# Import logging module for recording warning and error messages
import logging

# Define a function that extracts US market prices from HTML content
# Parameter: html (string) - the HTML content to parse
# Returns: dict - a dictionary containing market symbols as keys and their prices as values
def extract_us_market_prices(html: str) -> dict:
    # Parse the HTML content using BeautifulSoup with the html.parser engine
    soup = BeautifulSoup(html, "html.parser")

    # Create a dictionary mapping friendly column names to their corresponding financial symbols
    symbols = {
        "sp_futures": "^GSPC",           # S&P 500 futures
        "dow_futures": "^DJI",           # Dow Jones Index
        "nasdaq_futures": "^IXIC",       # NASDAQ Composite
        "gold": "GC=F",                  # Gold futures
        "crude_oil": "CL=F",             # Crude oil futures
        "russell_2000": "^RUT",          # Russell 2000 Index
        "vix": "^VIX"                    # Volatility Index
    }

    # Initialize an empty dictionary to store the results
    results = {}

    # Loop through each symbol in the symbols dictionary
    for column, symbol in symbols.items():
        # Find the HTML tag with fin-streamer element that matches both the data-symbol and data-field attributes
        tag = soup.find(
            "fin-streamer",
            {"data-symbol": symbol, "data-field": "regularMarketPrice"}
        )

        # Check if the tag was not found or if the text content is empty after stripping whitespace
        if not tag or tag.text.strip() == "":
            # Log a warning message indicating that the data for this column is missing
            logging.warning(f"{column} missing")
            # Set the result for this column to None
            results[column] = None
            # Skip to the next iteration of the loop
            continue

        # Extract the text content from the tag and remove leading/trailing whitespace
        text = tag.text.strip()

        # Try to convert the text to a float, removing commas first (for formatted numbers like "1,234.56")
        try:
            results[column] = float(text.replace(",", ""))
        # If the conversion fails, catch the ValueError exception
        except ValueError:
            # Log an error message with the column name and the invalid value that caused the error
            logging.error(f"{column} invalid value: {text}")
            # Set the result for this column to None
            results[column] = None

    # Return the results dictionary containing all extracted prices
    return results