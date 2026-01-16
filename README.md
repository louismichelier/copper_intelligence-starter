<<<<<<< HEAD
# Copper Intelligence – Starter

## Project Goal
Demonstrate a clean end-to-end data/analytics pipeline for Copper futures (HG=F).
Focus is on structure, readability, and data flow.

## Tech Stack
- **Language**: Python
- **Data Source**: yfinance (Yahoo Finance)
- **Database**: DuckDB (Local OLAP database)
- **Analysis**: Pandas (Moving Averages, Returns)
- **Visualization**: Streamlit (Dashboard)

## How to Run

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Data Pipeline**:
   This extracts data, cleans it, calculates indicators, and saves to DuckDB.
   ```bash
   python main.py
   ```

3. **Launch the Dashboard**:
   ```bash
   streamlit run app/dashboard.py
   ```

## Why Copper?
Copper is a leading economic indicator ("Dr. Copper"). Its price often correlates with global industrial demand, making it a strategic commodity for analysis.
=======