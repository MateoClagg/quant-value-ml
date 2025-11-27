"""
Initialize DuckDB Database

PURPOSE:
--------
Create DuckDB database and execute schema.sql to set up tables.

YOUR LEARNING TASKS:
-------------------
1. Connect to DuckDB (creates file if it doesn't exist)
2. Read and execute schema.sql
3. Verify tables were created
4. Optionally: Set up S3 extension for querying Parquet in S3

EXAMPLE STRUCTURE:
-----------------
import duckdb

def init_database(db_path: str):
    # Connect to DuckDB
    conn = duckdb.connect(db_path)

    # Install and load S3 extension
    conn.execute("INSTALL httpfs;")
    conn.execute("LOAD httpfs;")

    # Set S3 credentials (if querying S3 directly)
    conn.execute("SET s3_region='us-east-1';")
    conn.execute("SET s3_access_key_id='...';")
    conn.execute("SET s3_secret_access_key='...';")

    # Execute schema.sql
    with open('database/schema.sql', 'r') as f:
        schema = f.read()
    conn.executescript(schema)

    # Verify tables
    tables = conn.execute("SHOW TABLES").fetchall()
    print(f"Created tables: {tables}")

    return conn

QUESTIONS TO EXPLORE:
--------------------
- How big will your DuckDB file get? (Estimate based on 20GB Parquet)
- Should you configure memory_limit and threads?
- Do you need persistent config (duckdb.cfg file)?
- How to handle concurrent access (you + friend querying same DB)?

TIP: DuckDB is embedded, so no server to manage. Just a file!
"""

# TODO: Implement database initialization

if __name__ == "__main__":
    pass
