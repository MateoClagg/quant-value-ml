"""
Fundamentals Data Ingestion

PURPOSE:
--------
Fetch financial statements (income, balance sheet, cash flow) from EODHD.

YOUR LEARNING TASKS:
-------------------
1. Understand EODHD fundamentals endpoint structure
2. Parse nested JSON response (it's more complex than price data)
3. Normalize quarterly/annual data into tabular format
4. Store in S3 with appropriate partitioning

EODHD FUNDAMENTALS STRUCTURE:
-----------------------------
The fundamentals endpoint returns a large JSON with nested structures:
{
  "General": { company info },
  "Financials": {
    "Income_Statement": {
      "quarterly": { "2024-09-30": {...}, "2024-06-30": {...} },
      "yearly": { "2023-12-31": {...} }
    },
    "Balance_Sheet": { ... },
    "Cash_Flow": { ... }
  },
  "Valuation": { ratios },
  "Highlights": { key metrics }
}

YOUR TASK: Flatten this into DataFrames suitable for analysis.

SUGGESTED IMPLEMENTATION:
------------------------
Step 1: Fetch and explore
  - Get fundamentals for 1 ticker (e.g., AAPL)
  - Print the JSON, understand the structure
  - Use EODHD ChatGPT to clarify any fields

Step 2: Parse one statement type
  - Start with Income_Statement quarterly data
  - Convert to DataFrame with columns: symbol, fiscal_date, revenue, net_income, etc.
  - Save to Parquet

Step 3: Repeat for all statement types
  - Balance Sheet: assets, liabilities, equity, etc.
  - Cash Flow: operating_cf, investing_cf, financing_cf, fcf

Step 4: Scale to all tickers

EXAMPLE STRUCTURE:
-----------------
def fetch_fundamentals(symbol, client):
    # Fetch fundamentals JSON
    # Return parsed JSON
    pass

def parse_income_statement(fundamentals_json, symbol):
    # Extract quarterly income statements
    # Return DataFrame with schema:
    # [symbol, fiscal_date, revenue, gross_profit, operating_income, net_income, eps, ...]
    pass

def parse_balance_sheet(fundamentals_json, symbol):
    # Similar for balance sheet
    pass

def parse_cash_flow(fundamentals_json, symbol):
    # Similar for cash flow
    pass

QUESTIONS TO EXPLORE:
--------------------
- Do you want quarterly data, annual data, or both?
- How far back does EODHD provide fundamentals? (Usually 10-20 years)
- How to handle missing data (some companies don't report all fields)?
- Should you calculate derived metrics here (e.g., FCF = Operating CF - CapEx)?

DATA SCHEMA DECISIONS:
---------------------
Think about how you'll query this later:
- Wide format: Many columns (one per metric)
- Long format: Fewer columns (metric_name, metric_value)

For ML, wide format is usually easier.

TIP: Start with just Income Statement quarterly data for 10 tickers.
     Get that working end-to-end before adding more complexity.
"""

# TODO: Implement your fundamentals ingestion here

if __name__ == "__main__":
    pass
