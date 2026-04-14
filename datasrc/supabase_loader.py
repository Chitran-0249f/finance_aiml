
import os
import pandas as pd
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables from .env file
# This is where your SUPABASE_URL and SUPABASE_KEY are stored safely
load_dotenv()

# Read Supabase URL and API key from environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Create Supabase client object to interact with your database
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def load_market_data():
    """
    Load ALL rows from 'market_snapshots' table into a Pandas DataFrame.
    This handles the default 1000-row limit by fetching in batches.
    """

    data = []              # Initialize empty list to store rows from all batches
    offset = 0             # Start offset at 0 (first row)
    batch_size = 1000      # Number of rows to fetch per request (PostgREST default is 1000)

    # Loop until no more rows are returned
    while True:
        # Fetch a batch of rows from Supabase using range (offset to offset+batch_size-1)
        # This is like saying: "give me rows 0–999, then 1000–1999, etc."
        response = supabase.table("market_snapshots") \
            .select("*") \
            .range(offset, offset + batch_size - 1) \
            .execute()

        batch = response.data  # Extract actual rows from response

        # If no rows are returned, we have fetched all data; exit the loop
        if not batch:
            break

        # Add this batch to our main data list
        data.extend(batch)

        # Increment offset to fetch the next batch in the next loop iteration
        offset += batch_size

    # Convert the full list of rows into a Pandas DataFrame
    # This makes it easy to do EDA, feature engineering, plotting, etc.
    df = pd.DataFrame(data)

    # Return the complete DataFrame
    return df













# ---------------------- ADD GENERIC LOADER (REUSABLE) ---------------------


def load_table(table_name):
    """
    Generic loader to fetch ALL rows from ANY Supabase table
    
    This avoids rewriting the same logic for every table
    """
    
    data = []
    offset = 0
    batch_size = 1000
    
    while True:
        response = supabase.table(table_name) \
            .select("*") \
                .range(offset, offset + batch_size - 1) \
                .execute()
                
        batch = response.data
        
        if not batch:
            break
        
        data.extend(batch)
        offset += batch_size
        
    # Convert to Dataframe
    df = pd.DataFrame(data)

    return df









# ---------------------- STEP 2 — ADD FINANCIAL LOADERS ---------------------

def load_financial_tables():
    """
    
    Load all financial tables seperately for easier access in notebooks and ML scripts.
    
    """    

    reports_df = load_table("financial_reports")
    income_df = load_table("income_statements")
    balance_df = load_table("balance_sheets")
    cashflow_df = load_table("cash_flows")
    
    return reports_df, income_df, balance_df, cashflow_df











# ---------------------- STEP 3 — ADD JOINED DATASET (VERY IMPORTANT) ---------------------


def load_financial_dataset():
    """
    Load and JOIN all financial tables into one dataset
    """
    
    # Load individual tables
    reports_df, income_df, balance_df, cashflow_df = load_financial_tables()
    
    
    # Merge reports with income statements
    df = reports_df.merge(          # Start with financial_reports as the left table
        income_df,                  # Merge with income_statements as the right table
        left_on="id",           # Primary Key, Join on the report ID from financial_reports
        right_on="report_id",   # Foreign Key, Join on the report_id from income_statements
        how="left"      # Use left join to keep all financial_reports even if no matching income statement exists   
    )
    
    
    # Merge balance sheet
    df = df.merge(
        balance_df,
        left_on="id",
        right_on="report_id",
        how="left"
    )
    
    
    # Merge cash flow
    df = df.merge(
        cashflow_df,
        left_on="id",
        right_on="report_id",
        how="left"
    )
    
    
    return df













# ---------------------- NOW YOUR FILE LOOKS LIKE THIS ---------------------

#supabase_loader.py
#│
#├── supabase connection ✅
#├── load_market_data() ✅ (your existing one)
#├── load_table() ✅ (NEW reusable)
#├── load_financial_tables() ✅
#├── load_financial_dataset() ✅ ⭐

# ---------------------- N??????---------------------

# Why This Is Important
# Now:
# All database connection logic lives in one place
# Your notebook stays clean
# You can reuse this loader in ML scripts later

