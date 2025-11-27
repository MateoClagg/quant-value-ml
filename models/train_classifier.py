"""
XGBoost Value Investing Classifier

PURPOSE:
--------
Train a classification model to identify value stocks.

YOUR LEARNING TASKS:
-------------------
1. Define what "value stock" means (your target variable)
2. Load features from ml_features table
3. Train/test split (or time-series cross-validation)
4. Train XGBoost classifier
5. Evaluate performance and feature importance

TARGET VARIABLE OPTIONS:
-----------------------
Option 1: Forward returns
  - Label = 1 if 12-month forward return > S&P 500
  - Label = 0 otherwise

Option 2: Multiple criteria
  - Label = 1 if (low P/E AND low P/B AND positive FCF)
  - Based on value investing principles

Option 3: Piotroski-based
  - Label = 1 if Piotroski score >= 7
  - High-quality value stocks

EXAMPLE STRUCTURE:
-----------------
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

def prepare_training_data():
    # Query ml_features table
    # Handle missing values
    # Create labels
    pass

def train_model(X, y):
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(...)

    # Train XGBoost
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        max_depth=6,
        learning_rate=0.1,
        n_estimators=100
    )
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    print(classification_report(y_test, predictions))

    # Feature importance
    print(model.feature_importances_)

    return model

def save_model(model, path='models/value_classifier.json'):
    # Save for inference
    model.save_model(path)

QUESTIONS TO EXPLORE:
--------------------
- How to handle class imbalance (maybe few "value" stocks)?
- Time-series cross-validation vs random split?
- What features are most important?
- How to tune hyperparameters?
- Should you ensemble multiple models?

EVALUATION METRICS:
------------------
- Accuracy (basic, but can be misleading)
- Precision/Recall (more informative for imbalanced classes)
- ROC-AUC (overall discriminative power)
- Sharpe ratio of selected stocks (financial metric!)

TIP: Start simple. Binary classification with 10 features.
     Get the pipeline working before optimizing performance.
"""

# TODO: Implement your model training
