import duckdb
import os
from dotenv import load_dotenv

load_dotenv()

conn = duckdb.connect()
conn.execute("INSTALL httpfs; LOAD httpfs;")

# Set S3 credentials
conn.execute(f"SET s3_region='{os.getenv('AWS_REGION')}';")
conn.execute(f"SET s3_access_key_id='{os.getenv('AWS_ACCESS_KEY_ID')}';")
conn.execute(f"SET s3_secret_access_key='{os.getenv('AWS_SECRET_ACCESS_KEY')}';")

# Query your data!
bucket = os.getenv('S3_BUCKET')
result = conn.execute(f"""
    SELECT symbol, COUNT(*) as row_count, MIN(Date) as min_date, MAX(Date) as max_date
    FROM read_parquet('s3://{bucket}/stock-data/prices/**/*.parquet')
    GROUP BY symbol
    ORDER BY symbol
    LIMIT 20
""").df()

print(result)