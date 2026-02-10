import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def insert_market_snapshot(snapshot: dict):
    # snapshot keys MUST match table columns
    supabase.table("market_snapshots").insert(snapshot).execute()




