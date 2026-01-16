import yfinance as yf
import duckdb
import pandas as pd
import os

DB_PATH = os.path.join("data", "copper.duckdb")

def extract_data(ticker="HG=F", period="5y"):
    """
    Downloads data from yfinance and stores it in DuckDB.
    """
    print(f"Downloading {ticker} data for {period}...")
    df = yf.download(ticker, period=period, progress=False)
    
    # yfinance returns a MultiIndex column structure in newer versions or sometimes just columns.
    # We want to flatten it and ensure 'Date' is a column.
    df = df.reset_index()
    
    # Simple check to flattening columns if they are multi-level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] if col[1] == '' else f"{col[0]}_{col[1]}" for col in df.columns]
        
    # Standardize column names
    # yfinance typically gives: Date, Open, High, Low, Close, Adj Close, Volume
    # We rename them to snake_case for db
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]

    print(f"Downloaded {len(df)} rows.")

    # Connect to DuckDB
    con = duckdb.connect(DB_PATH)
    
    # Create or replace table
    print("Saving to DuckDB...")
    con.execute("CREATE OR REPLACE TABLE raw_prices AS SELECT * FROM df")
    
    con.close()
    print("Extraction complete.")

if __name__ == "__main__":
    extract_data()
