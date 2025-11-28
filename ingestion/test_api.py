# test_api.py (create this file temporarily)
import requests
import os
from dotenv import load_dotenv
import polars as pl
from io import StringIO



df = pl.read_parquet("data/prices/year=2024/prices.parquet")
print(df.head())