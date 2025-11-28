import time
import requests
import polars as pl
from io import StringIO

class EODHDClient:
    def __init__(self, api_key: str, rate_limit_delay: float = 0.06):
        self.api_key = api_key
        self.base_url = "https://eodhd.com/api"
        self.rate_limit_delay = rate_limit_delay

    def _throttle(self):
        time.sleep(self.rate_limit_delay)

    def get_eod_prices(self, symbol: str, start_date: str, end_date: str) -> pl.DataFrame:
        self._throttle()

        url = f"{self.base_url}/eod/{symbol}"
        params = {
            "api_token": self.api_key,
            "from": start_date,
            "to": end_date,
            "fmt": "csv"
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {symbol}: {e}")
            return pl.DataFrame()  # return empty DF for consistency

        try:
            df = pl.read_csv(StringIO(response.text))
            df = df.with_columns([
                pl.lit(symbol).alias("symbol")
            ])
            return df
        except Exception as e:
            print(f"[ERROR] Failed to parse CSV for {symbol}: {e}")
            return pl.DataFrame()
        
    def get_fundamentals(self, symbol: str, filter: str) -> dict:
        self._throttle()

        url = f"{self.base_url}/fundamentals/{symbol}"
        params = {
            "api_token": self.api_key,
            "filter": filter,
            "fmt": "json"
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to fetch {symbol}: {e}")
            return {}
        except ValueError as e:
            print(f"[ERROR] JSON decode failed for {symbol} | {filter}: {e}")
            return {}
        
    def get_all_fundamentals_quarterly(self, symbol: str) -> dict:
        filters = [
            "Financials::Income_Statement::quarterly",
            "Financials::Balance_Sheet::quarterly", 
            "Financials::Cash_Flow::quarterly"
        ]
        
        results = {}
        for filter_name in filters:
            data = self.get_fundamentals(symbol, filter_name)
            results[filter_name] = data
        
        return results
    
    def get_macro_indicator(self, country: str, indicator: str) -> list:
        self._throttle()

        url = f"{self.base_url}/macro-indicator-data"
        params = {
            "api_token": self.api_key,
            "country": country,
            "indicator": indicator,
            "fmt": "json"
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Macro indicator failed: {e}")
            return []
        
    def get_dividends(self, symbol: str, start_date: str, end_date: str) -> list:
        self._throttle()

        url = f"{self.base_url}/div/{symbol}"
        params = {
            "api_token": self.api_key,
            "from": start_date,
            "fmt": "json"
        }

        if end_date:
            params["to"] = end_date

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Dividends failed for {symbol}: {e}")
            return []
        
    def get_splits(self, symbol: str, start_date: str, end_date: str) -> list:
        self._throttle()

        url = f"{self.base_url}/splits/{symbol}"
        params = {
            "api_token": self.api_key,
            "from": start_date,
            "fmt": "json"
        }

        if end_date:
            params["to"] = end_date

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Splits failed for {symbol}: {e}")
            return []
        
    def get_distributions(self, symbol: str, start_date: str, end_date: str) -> dict:
        return {
            "dividends": self.get_dividends(symbol, start_date, end_date),
            "splits": self.get_splits(symbol, start_date, end_date)
        }






        
