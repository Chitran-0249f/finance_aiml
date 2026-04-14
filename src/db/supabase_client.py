"""
Supabase client module for interacting with the Supabase database.

This module provides functionality to connect to a Supabase instance
and perform database operations, such as inserting market snapshots.
"""

import os
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Supabase client using URL and API key from environment variables
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)


def insert_market_snapshot(snapshot: dict):
    """
    Insert a market snapshot into the 'market_snapshots' table.

    Args:
        snapshot (dict): A dictionary containing the market snapshot data.
                         Keys must match the table columns.

    Raises:
        Exception: If the insertion fails due to database errors.
    """
    # snapshot keys MUST match table columns
    supabase.table("market_snapshots").insert(snapshot).execute()




