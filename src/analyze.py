import duckdb
import pandas as pd
import os

DB_PATH = os.path.join("data", "copper.duckdb")

def generate_insights():
    """
    Generates simple rule-based insights from the processed data.
    """
    print("Generating insights...")
    con = duckdb.connect(DB_PATH)
    
    # Get the latest record
    # Assuming 'date' column exists, order by it.
    df = con.execute("SELECT * FROM processed_prices ORDER BY date DESC LIMIT 1").df()
    con.close()
    
    if df.empty:
        return "No data available."
    
    latest = df.iloc[0]
    price = latest['close']
    ma50 = latest['ma50']
    ma200 = latest['ma200']
    ret7 = latest['return_7d']
    
    insights = []
    insights.append(f"Current Price: {price:.2f}")
    
    # Trend Analysis
    if price > ma50 > ma200:
        insights.append("Trend: CLEAR UPTREND (Price > MA50 > MA200)")
    elif price < ma50 < ma200:
        insights.append("Trend: CLEAR DOWNTREND (Price < MA50 < MA200)")
    elif price > ma50 and price < ma200:
        insights.append("Trend: RECOVERY POSSIBLE (Price > MA50, but < MA200)")
    else:
        insights.append("Trend: SIDEWAYS / MIXED")
        
    # Momentum
    if ret7 > 0.05:
        insights.append("Momentum: STRONG GREEN (7d return > 5%)")
    elif ret7 < -0.05:
        insights.append("Momentum: STRONG RED (7d return < -5%)")
    else:
         insights.append(f"Momentum: Neutral (7d return: {ret7:.1%})")
         
    return "\n".join(insights)

if __name__ == "__main__":
    print(generate_insights())
