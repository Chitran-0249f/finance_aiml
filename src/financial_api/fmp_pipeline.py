
# Import function that fethches data from the API
from src.financial_api.fmp_client import fetch_data

# Import Supabase connection (used to insert data into database)
from src.db.supabase_client import supabase


# Import time to add delay between API calls (avoid rate limit)
import time


def run_fmp_pipeline():
    """
    This function runs the financial API pipeline
    It fetches financial data for a list of companies and inserts it into the Supabase database.
    """
    
    #List of stock symbols or companies we want to process
    symbols = ["AAPL", "ADBE", "NVDA"]  # You can add more symbols as needed
    
    # Loop thorugh each company one by one
    for symbol in symbols:
        
        # Loop throuigh each type of financial statement
        for statement_type in [
            
            "income-statement",              # This is the profit and loss statement or data, showing revenues, expenses, and net income.
            "balance-sheet-statement",       # This shows the company's assets, liabilities, and shareholders' equity at a specific point in time.
            "cash-flow-statement"           # This shows the cash movement or inflows and outflows from operating, investing, and financing activities.
        ]:
            
            # Call API function to get data for this symbol and statement type
            data = fetch_data(symbol, statement_type)
            
            
            # Loop through each record returned by API (each year/quater)
            for record in data:
                
                
                # ---------------- STEP 1: SAVE RAW JSON ----------------
                # Store the full API response (unchanged) in database
                # This is useful for debugging and auditing later
                
                supabase.table("financial_statements_raw").insert({
                    
                    "symbol": symbol,               # The stock symbol (e.g., AAPL) to identify the company
                    "statement_type": statement_type,           # The type of financial statement (e.g., income-statement)
                    "data": record              # The full JSON record from the API, stored as-is for future reference (e.g., {"date": "2023-12-31", "revenue": 1000000, ...
                    }).execute() # Execute the insert operation to save the raw data into the database
                
                
                
                # ---------------- STEP 2: SAVE SHARED DATA ----------------
                # Insert common fields into main table
                
                report = supabase.table("financial_reports").insert({
                    
                    "symbol": symbol,           # The stock symbol (e.g., AAPL) to identify the company
                    "statement_type": statement_type,           # The type of financial statement (e.g., income-statement)      
                    "report_date": record["date"],      # The date of the financial report (e.g., "2023-12-31") extracted from the API record
                    "period": record["period"]          # The reporting period (e.g., "FY" for full year or "Q1" for first quarter) extracted from the API record
                    
                }).execute()        # Execute the insert operation to save the shared data into the main financial_reports table and get the inserted record's ID for linking with metrics
                
                
                
                # Extract the ID of the newly inserted report to link with metrics
                # This ID is used to link other tables (VERY IMPORTANT)
                report_id = report.data[0]["id"]  # Get the ID of the inserted report (assuming the first record in the response is the one we just inserted
                
                
                
                # ---------------- STEP 3: MAP DATA TO CORRECT TABLE ----------------
                
                # If the data is from income statement
                if statement_type == "income-statement":
                    
                    # Insert selected fields into income table
                    supabase.table("income_statements").insert({
                        
                        "report_id": report_id,
                        # foreign key linking to financial_reports table
                        
                        "revenue": record["revenue"],
                        # take "revenue" from API JSON
                        
                        "net_income": record["netIncome"],
                        # take "netIncome" from API JSON
                        # API uses camelCase → DB uses snake_case
                        
                        "gross_profit": record["grossProfit"],
                        # take "grossProfit" from API JSON
                        
                        "eps": record["eps"]    
                        # take "eps" (earnings per share) from API JSON
                        
                    }).execute() # Execute the insert operation to save the income statement metrics into the database
                    
                    
                # If the data is from balance sheet
                elif statement_type == "balance-sheet-statement":
                    
                    
                    # Insert selected fields into balance table
                    supabase.table("balance_sheets").insert({
                        
                        "report_id": report_id,  # foreign key linking to financial_reports table
                        
                        "total_assets": record["totalAssets"],  # take "totalAssets" from API JSON
                        
                        "total_liabilities": record["totalLiabilities"],  # take "totalLiabilities" from API JSON
                        
                        "total_equity": record["totalEquity"],  # take "shareholdersEquity" from API JSON
                        
                        "total_debt": record["totalDebt"]  # take "totalDebt" from API JSON
                        
                    }).execute()    # Execute the insert operation to save the balance sheet metrics into the database
                
                
                # If the data is from cash flow
                elif statement_type == "cash-flow-statement":
                    
                    
                    # Insert selected fields into cash flow table
                    supabase.table("cash_flows").insert({
                        
                        "report_id": report_id, # foreign key linking to financial_reports table
                        
                        "operating_cash_flow": record["operatingCashFlow"],   # take "operatingCashFlow" from API JSON
                        
                        "free_cash_flow": record["freeCashFlow"],   # take "freeCashFlow" from API JSON
                        
                        "capital_expenditure": record["capitalExpenditure"]    # take "capitalExpenditure" from API JSON   
                        
                    }).execute()    # Execute the insert operation to save the cash flow metrics into the database
                    
                    
            # Print a message to console after processing each symbol and statement type
            # Print progress so you know pipeline is working
            print(f"{symbol} - {statement_type} inserted")

            # Avoid API rate limit
            time.sleep(1)