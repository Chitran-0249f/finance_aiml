import os
import time
from src.scraper.yahoo_scraper_updated import scrape_yahoo_home
from src.db.supabase_client import insert_market_snapshot

# -----------------------------
# Setup dynamic log file path
# -----------------------------
# This ensures the log file is always created in your project folder
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(PROJECT_ROOT, "pipeline.log")

def run_pipeline(interval_seconds=30):
    """
    Continuous pipeline for scraping Yahoo Finance data and saving to Supabase.

    Parameters:
        interval_seconds (int): Time to wait between successful scrapes.
    """

    print("Pipeline started. Logs will be written to:", LOG_FILE)

    while True:
        try:
            # -----------------------------
            # Scrape the data
            # -----------------------------
            data = scrape_yahoo_home()

            # -----------------------------
            # Insert into Supabase
            # -----------------------------
            insert_market_snapshot(data)

            # -----------------------------
            # Print to console and append to log file
            # -----------------------------
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} - Saved: {data}")

            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp} - Saved: {data}\n")

            # -----------------------------
            # Wait before next scrape
            # -----------------------------
            time.sleep(interval_seconds)

        except Exception as e:
            # -----------------------------
            # Log any errors and continue
            # -----------------------------
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{timestamp} - Pipeline error: {e}")

            with open(LOG_FILE, "a") as f:
                f.write(f"{timestamp} - Pipeline error: {e}\n")

            # Wait a bit before retrying after an error
            time.sleep(10)
