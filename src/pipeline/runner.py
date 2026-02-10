import time
from src.scraper.yahoo_scraper_updated import scrape_yahoo_home
from src.db.supabase_client import insert_market_snapshot

def run_pipeline(interval_seconds=1):
    while True:
        try:
            data = scrape_yahoo_home()
            insert_market_snapshot(data)
            print("Saved:", data)
            time.sleep(interval_seconds)

        except Exception as e:
            print("Pipeline error:", e)
            time.sleep(5)
