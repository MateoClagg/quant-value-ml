import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import polars as pl
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm

from eodhd_client import EODHDClient


def format_symbol(symbol: str, exchange: str = "US") -> str:
    if f".{exchange}" not in symbol:
        return f"{symbol}.{exchange}"
    return symbol


def load_tickers(ticker_file: str) -> list[str]:
    with open(ticker_file, 'r') as file:
        tickers = [line.strip() for line in file if line.strip()]
    
    # Format with exchange suffix
    return [format_symbol(ticker) for ticker in tickers]


def fetch_prices_for_tickers(
    client: EODHDClient, 
    tickers: list[str], 
    start_date: str, 
    end_date: str
) -> tuple[pl.DataFrame, dict]: 
    
    all_data = []
    failed_tickers = []
    successful_tickers = []

    for ticker in tqdm(tickers):
        df = client.get_eod_prices(ticker, start_date, end_date)
        if df.height > 0:
            all_data.append(df)
            successful_tickers.append(ticker)
        else:
            failed_tickers.append(ticker)

    if not all_data:
        print("[ERROR] No data fetched for any ticker")
        return pl.DataFrame(), {"success": 0, "failed": len(tickers), "failed_tickers": failed_tickers}

    combined_df = pl.concat(all_data)
    summary = {
        "total_tickers": len(tickers),
        "successful": len(successful_tickers),
        "failed": len(failed_tickers),
        "failed_tickers": failed_tickers,
        "total_rows": len(combined_df),
    }

    return combined_df, summary


def partition_and_save_local(df: pl.DataFrame, output_dir: str):
    """
    Save DataFrame to partitioned Parquet files locally.
    Partitions by year: data/prices/year=2024/prices.parquet
    """
    df = df.with_columns([
        pl.col("Date").str.strptime(pl.Date, "%Y-%m-%d").alias("date_parsed")
    ]).with_columns([
        pl.col("date_parsed").dt.year().alias("year")
    ])
    
    # Create partitioned directory structure
    for(year,), group_df in df.group_by(["year"]):
        partition_dir = Path(output_dir) / f"year={year}"
        partition_dir.mkdir(parents=True, exist_ok=True)

        # Drop unneeded helper columns
        clean_df = group_df.drop(["date_parsed", "year"])

        output_file = partition_dir / "prices.parquet"
        clean_df.write_parquet(
            output_file,
            compression="snappy"
        )

        print(f"✓ Saved {len(clean_df):,} rows to {output_file}")


def upload_to_s3(local_dir: str, s3_bucket: str, s3_prefix: str):
    # Initialize s3 client
    s3_client = boto3.client('s3')

    local_path = Path(local_dir)

    # Find all parquet files recursively
    parquet_files = list(local_path.rglob("*.parquet"))

    if not parquet_files:
        print(f"[WARNING] No parquet files found in {local_dir}")
        return
    
    print(f"Found {len(parquet_files)} files to upload")

    # Upload each file
    for parquet_file in parquet_files:
        # Get path relative to local_dir (e.g. year=2024/prices.parquet)
        relative_path = parquet_file.relative_to(local_path)
        
        # Build S3 key (path in S3)
        # Replace backslashes with forward slashes (Windows compatibility)
        s3_key = f"{s3_prefix}/{relative_path}".replace("\\", "/")

        try:
            print(f"  Uploading {relative_path} → s3://{s3_bucket}/{s3_key}")
            s3_client.upload_file(
                Filename=str(parquet_file),
                Bucket=s3_bucket,
                Key=s3_key
            )
        except ClientError as e:
            print(f"  [ERROR] Failed to upload {parquet_file}: {e}")
            # Continue with other files even if one fails
        
    print(f"✓ Upload complete to s3://{s3_bucket}/{s3_prefix}")


def main():
    import time
    start_time = time.time()
    # Load environment variables
    load_dotenv()
    
    # Configuration
    api_key = os.getenv("EODHD_API_KEY")
    s3_bucket = os.getenv("S3_BUCKET")
    ticker_file = "config/tickers.txt"
    start_date = "2005-01-01"  # 20 years back
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize client
    client = EODHDClient(api_key)
    
    # Load tickers
    tickers = load_tickers(ticker_file)
    print(f"Loaded {len(tickers)} tickers")
    
    print(f"\n{'='*60}")
    print(f"EODHD Price Data Ingestion")
    print(f"{'='*60}")
    print(f"Tickers: {len(tickers)}")
    print(f"Date range: {start_date} to {end_date}")
    print(f"{'='*60}\n")
    
    # Fetch data
    df, summary = fetch_prices_for_tickers(client, tickers, start_date, end_date)
    
    # Save locally
    local_output = "data/prices"
    partition_and_save_local(df, local_output)
    
    # Upload to S3
    if s3_bucket:
        upload_to_s3(local_output, s3_bucket, "stock-data/prices")
    
    # Print summary
    elapsed = time.time() - start_time
    print(f"\n{'='*60}")
    print(f"INGESTION SUMMARY")
    print(f"{'='*60}")
    print(f"Total tickers: {summary['total_tickers']}")
    print(f"✓ Successful: {summary['successful']}")
    print(f"✗ Failed: {summary['failed']}")
    print(f"Total rows ingested: {summary['total_rows']:,}")
    print(f"Time elapsed: {elapsed/60:.1f} minutes")
    print(f"{'='*60}")
    
    if summary['failed_tickers']:
        print(f"\nFailed tickers: {', '.join(summary['failed_tickers'])}")
        # Save failed tickers to file for retry
        with open("data/failed_tickers.txt", "w") as f:
            f.write("\n".join(summary['failed_tickers']))
        print("Failed tickers saved to data/failed_tickers.txt")


if __name__ == "__main__":
    main()
