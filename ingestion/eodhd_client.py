"""
EODHD API Client

PURPOSE:
--------
This module will be your wrapper around the EODHD API with built-in:
- Rate limiting (1000 req/min, 100k req/day)
- Retry logic for failed requests
- Error handling and logging
- Response parsing

YOUR LEARNING TASKS:
-------------------
1. Create an EODHDClient class that:
   - Takes API key from environment variables
   - Has methods like get_eod_prices(), get_fundamentals()
   - Implements rate limiting (hint: use tenacity or asyncio.Semaphore)
   - Handles HTTP errors gracefully

2. Use EODHD's ChatGPT assistant to understand:
   - EOD prices endpoint format and parameters
   - Fundamentals endpoint structure
   - How to request bulk data efficiently
   - Date range parameters

3. Consider async vs sync:
   - Start with synchronous requests (easier to debug)
   - Later optimize with aiohttp for parallel fetching

EXAMPLE STRUCTURE:
-----------------
class EODHDClient:
    def __init__(self, api_key: str):
        # Initialize with API key, setup rate limiter
        pass

    def get_eod_prices(self, symbol: str, start_date: str, end_date: str):
        # Fetch historical EOD prices for a symbol
        # Returns: DataFrame or dict
        pass

    def get_fundamentals(self, symbol: str):
        # Fetch company fundamentals (income stmt, balance sheet, etc.)
        pass

    def _make_request(self, url: str, params: dict):
        # Internal method to handle actual HTTP request
        # Include rate limiting here
        pass

QUESTIONS TO EXPLORE:
--------------------
- What's the URL format for EOD prices?
- What parameters are required/optional?
- What does the JSON response look like?
- How should you handle API errors (429 rate limit, 404 not found)?
- Should you cache responses to avoid re-fetching?

RESOURCES:
---------
- EODHD API docs: https://eodhd.com/financial-apis/
- Use their ChatGPT assistant for specific endpoint questions
- tenacity library docs for retry logic
"""

# TODO: Implement your EODHDClient class here
