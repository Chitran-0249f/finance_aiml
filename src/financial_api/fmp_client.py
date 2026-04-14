# This API Client file is used to EXTRACT DATA

# Import library to call API
import requests  

# Import tools for environment variables
import os
from dotenv import load_dotenv  


# Load environment variables from .env file
load_dotenv()  


# Get API key securely from .env
API_KEY = os.getenv("FMP_API_KEY")  


# Use STABLE endpoint (since this works for you in Postman)
BASE_URL = "https://financialmodelingprep.com/stable"  


def fetch_data(symbol, statement_type):
    """
    Fetch financial data from API

    symbol: AAPL, ADBE, NVDA
    statement_type:
        income-statement
        balance-sheet-statement
        cash-flow-statement
    """

    # Build URL WITHOUT symbol (IMPORTANT for /stable)
    url = f"{BASE_URL}/{statement_type}"  

    # Parameters sent with request
    params = {
        "symbol": symbol,   # symbol goes here (NOT in URL)
        "apikey": API_KEY
    }

    # Debug print (VERY IMPORTANT for debugging APIs)
    print("Request URL:", url)
    print("Params:", params)


    # Send request to API
    response = requests.get(url, params=params)  


    # Print status code for debugging
    print("Status Code:", response.status_code)


    # If request failed, print error before crashing
    if response.status_code != 200:
        print("Error Response:", response.text)


    # Raise error if request failed
    response.raise_for_status()  


    # Convert JSON response into Python dictionary/list
    data = response.json()  


    # Return data to pipeline
    return data  