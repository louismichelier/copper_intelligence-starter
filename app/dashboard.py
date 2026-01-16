import streamlit as st
import duckdb
import pandas as pd
import os
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Copper Intelligence", layout="wide")

DB_PATH = os.path.join("data", "copper.duckdb")

def load_data():
    con = duckdb.connect(DB_PATH)
    # Check if table exists
    tables = con.execute("SHOW TABLES").fetchall()
    if not tables or ('processed_prices',) not in tables:
        con.close()
        return None
    
    df = con.execute("SELECT * FROM processed_prices ORDER BY date ASC").df()
    con.close()
    return df

def main():
    st.title("🔩 Copper Intelligence Starter")
    st.markdown("Analyzing Copper Futures (HG=F) with DuckDB and Python")
    
    df = load_data()
    
    if df is None:
        st.warning("Data not found. Please run `python main.py` first to generate the database.")
        if st.button("Run Pipeline Now"):
            import subprocess
            subprocess.run(["python", "main.py"])
            st.experimental_rerun()
        return

    # Key Metrics
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    price_col = 'close'
    current_price = latest[price_col]
    prev_price = prev[price_col]
    delta = current_price - prev_price
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Copper Price", f"${current_price:.4f}", f"{delta:.4f}")
    col2.metric("50-Day MA", f"${latest['ma50']:.4f}")
    col3.metric("200-Day MA", f"${latest['ma200']:.4f}")

    # Charting
    st.subheader("Price History & Trends")
    
    # We use Plotly for a better chart than st.line_chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df[price_col], mode='lines', name='Price', line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=df['date'], y=df['ma50'], mode='lines', name='50-Day MA', line=dict(color='blue', width=1)))
    fig.add_trace(go.Scatter(x=df['date'], y=df['ma200'], mode='lines', name='200-Day MA', line=dict(color='red', width=1)))
    
    fig.update_layout(height=500, xaxis_title="Date", yaxis_title="Price (USD)", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Simple Analysis / Insights Section
    st.subheader("Automated Insights")
    
    insights = []
    if current_price > latest['ma50'] > latest['ma200']:
        insights.append("✅ **Technically Bullish**: Price is above both moving averages, and 50MA > 200MA.")
    elif current_price < latest['ma50'] < latest['ma200']:
        insights.append("🔻 **Technically Bearish**: Price is below both moving averages.")
    
    if latest['return_7d'] > 0:
        insights.append(f"📈 **Positive Momentum**: Up {latest['return_7d']:.1%} in the last 7 days.")
    else:
        insights.append(f"📉 **Negative Momentum**: Down {latest['return_7d']:.1%} in the last 7 days.")
        
    for i in insights:
        st.write(i)

    # Data Source
    with st.expander("View Raw Data"):
        st.dataframe(df.sort_values(by='date', ascending=False).head(100))

if __name__ == "__main__":
    main()
