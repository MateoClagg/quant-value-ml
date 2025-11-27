"""
Fundamental Ratio Feature Engineering

PURPOSE:
--------
Calculate financial ratios for value investing from fundamentals data.

YOUR LEARNING TASKS:
-------------------
1. Join price data with fundamentals (as-of date matching)
2. Calculate standard financial ratios
3. Handle quarterly vs annual reporting
4. Deal with missing/negative values

SUGGESTED VALUE INVESTING RATIOS:
---------------------------------
1. Valuation multiples:
   - P/E ratio (Price / Earnings per share)
   - P/B ratio (Price / Book value per share)
   - P/S ratio (Price / Sales per share)
   - EV/EBITDA

2. Profitability:
   - ROE (Return on Equity)
   - ROA (Return on Assets)
   - Gross margin, Operating margin, Net margin

3. Financial health:
   - Debt-to-Equity ratio
   - Current ratio (Current Assets / Current Liabilities)
   - Quick ratio
   - Interest coverage

4. Cash flow:
   - Free Cash Flow yield
   - Operating Cash Flow / Net Income

5. Value signals:
   - Piotroski F-Score (9-point quality scale)
   - Graham Number (intrinsic value)
   - Magic Formula rank (Greenblatt)

EXAMPLE IMPLEMENTATION:
----------------------
def calculate_pe_ratio(prices_df, income_df):
    # Join price with most recent EPS
    # Handle negative earnings (P/E undefined)
    pass

def calculate_piotroski_score(fundamentals):
    # 9 binary criteria (profitability, leverage, operating efficiency)
    # Score 0-9, higher is better quality
    # See: https://en.wikipedia.org/wiki/Piotroski_F-Score
    pass

QUESTIONS TO EXPLORE:
--------------------
- How to handle point-in-time correctness?
  (Don't use future fundamentals that weren't available yet)
- TTM (Trailing Twelve Months) vs MRQ (Most Recent Quarter)?
- What to do with negative/zero denominators?
- Should you filter out financials/REITs (different accounting)?

POINT-IN-TIME CORRECTNESS IS CRITICAL:
-------------------------------------
Bad:  Use Q3 2024 earnings to calculate features for Sept 2024
Good: Use Q2 2024 earnings (last available) for Sept 2024

Companies report earnings ~45 days after quarter end.
You need to lag fundamentals appropriately!

TIP: Start with simple ratios (P/E, P/B, ROE).
     Test with a few tickers to verify calculations match public data.
"""

# TODO: Implement fundamental ratio calculations
