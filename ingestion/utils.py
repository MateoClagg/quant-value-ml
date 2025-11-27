"""
Shared utilities for ingestion scripts

PURPOSE:
--------
Common helper functions used across ingestion scripts.

SUGGESTED UTILITIES:
-------------------
1. load_tickers() - Read tickers from config file
2. get_s3_client() - Initialize boto3 S3 client
3. upload_to_s3() - Upload file to S3 with proper path
4. get_date_range() - Calculate start/end dates for backfill
5. validate_dataframe() - Basic data quality checks

YOUR LEARNING TASK:
------------------
Implement helper functions that reduce code duplication.
Think about what you'll need in multiple places.
"""

# TODO: Add your utility functions here

def load_tickers(filepath: str) -> list:
    """
    Load ticker list from file.

    Args:
        filepath: Path to tickers.txt

    Returns:
        List of ticker symbols

    HINT: Handle comments (#) and empty lines
    """
    pass


def validate_price_data(df):
    """
    Validate price DataFrame has required columns and reasonable values.

    Checks:
    - Required columns exist (date, open, high, low, close, volume)
    - No nulls in critical columns
    - High >= Low
    - Prices > 0

    HINT: Use pandas/polars validation methods
    """
    pass
