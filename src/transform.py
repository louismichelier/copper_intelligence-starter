import duckdb
import pandas as pd
import os

DB_PATH = os.path.join("data", "copper.duckdb")

def transform_data():
    """
    Reads raw data, cleans it, calculates indicators, and saves to processed_prices.
    """
    print("Starting transformation...")
    con = duckdb.connect(DB_PATH)
    
    # Load raw data
    df = con.execute("SELECT * FROM raw_prices ORDER BY date ASC").df()
    
    # 1. Clean data: Ensure date is datetime, handle missing values
    # yfinance usually returns good data, but we forward fill just in case for trading days
    df = df.ffill()
    
    # 2. Calculate Indicators
    # 2. Calculate Indicators
    # Dynamically find the price column (handle 'Close', 'close', 'adj_close', or ticker-suffixed variants)
    price_col = None
    candidates = [c for c in df.columns if 'close' in c.lower()]
    
    # Priority: exact 'close', then 'adj_close', then shortest column name containing 'close'
    if 'close' in df.columns:
        price_col = 'close'
    elif 'adj_close' in df.columns:
        price_col = 'adj_close'
    elif candidates:
        # Pick the shortest one (likely "Close_Ticker" vs "Adj_Close_Ticker", usually we want Close)
        # But 'adj' might be better for returns. Let's strictly follow "Close" preference from user prompt for now if available.
        # Check for one without 'adj' first
        non_adj = [c for c in candidates if 'adj' not in c.lower()]
        if non_adj:
             price_col = min(non_adj, key=len)
        else:
             price_col = min(candidates, key=len)
    
    if not price_col:
        # Fallback to any column if we can't find 'close' - maybe 'price'?
        raise ValueError(f"Could not identify a price column from: {df.columns.tolist()}")

    print(f"Selected price column: {price_col}")

    # Standardize to 'close' for downstream consistency
    if price_col != 'close':
        df = df.rename(columns={price_col: 'close'})
        price_col = 'close'
    
    df['ma50'] = df[price_col].rolling(window=50).mean()
    df['ma200'] = df[price_col].rolling(window=200).mean()
    
    # 7-day percentage return
    df['return_7d'] = df[price_col].pct_change(periods=7)
    
    # Drop existing processed table
    con.execute("DROP TABLE IF EXISTS processed_prices")
    
    # Save processed data
    # We can register the dataframe and create table from it
    con.register('df_processed', df)
    con.execute("CREATE TABLE processed_prices AS SELECT * FROM df_processed")
    
    con.close()
    print("Transformation complete.")

if __name__ == "__main__":
    transform_data()
