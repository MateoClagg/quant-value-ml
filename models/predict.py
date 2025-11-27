"""
Model Inference / Prediction

PURPOSE:
--------
Use trained XGBoost model to classify stocks as value/not-value.

YOUR LEARNING TASKS:
-------------------
1. Load trained model
2. Query latest features from DuckDB
3. Generate predictions
4. Output ranked list of value stocks

EXAMPLE STRUCTURE:
-----------------
import xgboost as xgb
import duckdb

def load_model(path='models/value_classifier.json'):
    model = xgb.Booster()
    model.load_model(path)
    return model

def get_latest_features():
    # Query DuckDB for most recent features
    conn = duckdb.connect('data/stocks.duckdb')
    df = conn.execute('''
        SELECT * FROM ml_features
        WHERE date = (SELECT MAX(date) FROM ml_features)
    ''').df()
    return df

def predict_value_stocks(model, features_df):
    # Generate predictions
    X = features_df[FEATURE_COLUMNS]
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    # Rank by probability
    results = features_df[['symbol']].copy()
    results['value_score'] = probabilities
    results = results.sort_values('value_score', ascending=False)

    return results

USE CASE:
--------
Run this script daily/weekly to get:
- Top 50 value stocks by score
- Watchlist for further research
- Portfolio rebalancing signals

OUTPUT FORMAT:
-------------
symbol | value_score | pe_ratio | pb_ratio | piotroski_score
AAPL   | 0.87        | 25.3     | 45.2     | 8
MSFT   | 0.82        | 30.1     | 12.5     | 7
...
"""

# TODO: Implement prediction script

if __name__ == "__main__":
    pass
