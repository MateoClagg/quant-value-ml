"""
EOD Price Data Ingestion

PURPOSE:
--------
Fetch historical end-of-day price data from EODHD and store in S3 as Parquet.

YOUR LEARNING TASKS:
-------------------
1. Read ticker list from config/tickers.txt
2. Use EODHDClient to fetch price data for each ticker
3. Transform API response to Polars/Pandas DataFrame
4. Write DataFrame to Parquet with partitioning (year/month)
5. Upload to S3 with proper folder structure

SUGGESTED IMPLEMENTATION STEPS:
-------------------------------
Step 1: Start small (local testing)
  - Fetch 1 ticker, 1 year of data
  - Print the response, understand the structure
  - Convert to DataFrame

Step 2: Write to local Parquet
  - Save DataFrame to data/prices/year=2024/month=01/AAPL.parquet
  - Test reading it back with DuckDB

Step 3: Add S3 upload
  - Use boto3 to upload Parquet files
  - Maintain same folder structure

Step 4: Scale to multiple tickers
  - Loop through ticker list
  - Add progress tracking (tqdm library)
  - Handle errors (some tickers may fail)

Step 5: Add checkpointing
  - Track which tickers are already ingested
  - Resume from failures

EXAMPLE STRUCTURE:
-----------------
def main():
    # 1. Load config (API key, S3 bucket, date range)
    # 2. Initialize EODHD client
    # 3. Read ticker list
    # 4. For each ticker:
    #    - Fetch data
    #    - Transform to DataFrame
    #    - Write Parquet (partitioned by year/month)
    #    - Upload to S3
    # 5. Log summary (success/failures)

def fetch_and_save_ticker(symbol, client, start_date, end_date):
    # Fetch data for one ticker
    # Return success/failure status
    pass

QUESTIONS TO EXPLORE:
--------------------
- Should you fetch all 20 years in one request, or batch by year?
- How to partition Parquet files? (By ticker? By date? Both?)
- What columns do you need? (date, open, high, low, close, adj_close, volume)
- How to handle corporate actions (splits, dividends)?
- Should you validate data before saving?

DATA PARTITIONING STRATEGY:
--------------------------
Option A: s3://bucket/prices/symbol=AAPL/year=2024/month=01/data.parquet
Option B: s3://bucket/prices/year=2024/month=01/AAPL.parquet
Option C: s3://bucket/prices/year=2024/month=01/all_tickers.parquet

Think about:
- Query patterns (filter by ticker? by date?)
- File size (too many small files = slow, too large = memory issues)
- Scalability (1000 tickers now, maybe 10k later?)

TIP: Start with Option B, it's simple and works well for this scale.
"""

# TODO: Implement your ingestion script here

if __name__ == "__main__":
    # Your main entry point
    pass
