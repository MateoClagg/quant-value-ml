-- Example DuckDB Queries for Stock Analysis
--
-- PURPOSE: Provide query examples for you and your friend to explore data
-- Run these in DuckDB CLI or Python (duckdb.execute())

-- ============================================================================
-- BASIC QUERIES
-- ============================================================================

-- Get price history for a specific stock
SELECT * FROM prices
WHERE symbol = 'AAPL'
ORDER BY date DESC
LIMIT 100;

-- Latest prices for all stocks
SELECT
    symbol,
    date,
    close,
    volume
FROM prices
WHERE date = (SELECT MAX(date) FROM prices)
ORDER BY symbol;

-- ============================================================================
-- QUERYING S3 PARQUET DIRECTLY (Zero-copy)
-- ============================================================================

-- Read prices from S3 without loading into DuckDB table
-- Replace with your actual S3 bucket path
SELECT * FROM read_parquet('s3://your-bucket/stock-data/prices/year=2024/**/*.parquet')
WHERE symbol = 'AAPL'
LIMIT 10;

-- Create view from S3 (both you and friend can use same S3 data)
CREATE OR REPLACE VIEW prices_s3 AS
SELECT * FROM read_parquet('s3://your-bucket/stock-data/prices/**/*.parquet');

-- Now query the view
SELECT * FROM prices_s3
WHERE symbol IN ('AAPL', 'MSFT', 'GOOGL')
AND date >= '2024-01-01';

-- ============================================================================
-- ANALYTICAL QUERIES
-- ============================================================================

-- Calculate returns for all stocks
SELECT
    symbol,
    date,
    close,
    LAG(close) OVER (PARTITION BY symbol ORDER BY date) as prev_close,
    (close / LAG(close) OVER (PARTITION BY symbol ORDER BY date) - 1) * 100 as daily_return
FROM prices
WHERE date >= '2024-01-01'
ORDER BY symbol, date;

-- Top performers YTD
SELECT
    symbol,
    MIN(CASE WHEN date = '2024-01-02' THEN close END) as year_start_price,
    MAX(CASE WHEN date = (SELECT MAX(date) FROM prices) THEN close END) as current_price,
    (MAX(CASE WHEN date = (SELECT MAX(date) FROM prices) THEN close END) /
     MIN(CASE WHEN date = '2024-01-02' THEN close END) - 1) * 100 as ytd_return
FROM prices
WHERE date >= '2024-01-01'
GROUP BY symbol
ORDER BY ytd_return DESC
LIMIT 20;

-- ============================================================================
-- FUNDAMENTAL ANALYSIS
-- ============================================================================

-- Latest fundamentals for all companies
SELECT
    symbol,
    fiscal_date,
    revenue,
    net_income,
    (net_income / revenue * 100) as net_margin
FROM income_statement
WHERE fiscal_date = (
    SELECT MAX(fiscal_date)
    FROM income_statement i2
    WHERE i2.symbol = income_statement.symbol
)
ORDER BY net_margin DESC;

-- Companies with strong balance sheets
SELECT
    symbol,
    fiscal_date,
    (current_assets / current_liabilities) as current_ratio,
    (total_equity / total_assets) as equity_ratio
FROM balance_sheet
WHERE fiscal_date = (
    SELECT MAX(fiscal_date)
    FROM balance_sheet b2
    WHERE b2.symbol = balance_sheet.symbol
)
AND current_assets / current_liabilities > 2  -- Healthy liquidity
AND total_equity / total_assets > 0.5         -- Low leverage
ORDER BY current_ratio DESC;

-- ============================================================================
-- VALUE INVESTING SCREENS
-- ============================================================================

-- Low P/E, positive earnings stocks
SELECT
    f.symbol,
    f.pe_ratio,
    f.pb_ratio,
    f.roe,
    f.piotroski_score
FROM ml_features f
WHERE f.date = (SELECT MAX(date) FROM ml_features)
AND f.pe_ratio < 15
AND f.pe_ratio > 0
AND f.roe > 0.15
ORDER BY f.piotroski_score DESC, f.pe_ratio ASC
LIMIT 50;

-- TODO: Add your own custom screens based on your value investing criteria
