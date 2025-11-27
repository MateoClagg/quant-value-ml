# 📊 EODHD Stock Data Pipeline

> **Simple, local-first pipeline** - EODHD API → S3 Parquet → DuckDB → XGBoost value investing classifier

## 🎯 **Project Goals**

Build a cost-effective, scalable data pipeline for:
- **20 years** of historical EOD price data
- **1000 tickers** (expandable)
- **Financial statements** (income, balance sheet, cash flow)
- **Value investing model** (XGBoost classification)
- **Easy collaboration** (S3-backed, SQL queries)

## 🏗️ **Architecture**

```
EODHD API ($100/month)
  100k requests/day, 1k req/min
         ↓
  Python Ingestion
  (async, rate-limited)
         ↓
    S3 Parquet Files
  (partitioned by date)
    ├── prices/
    ├── fundamentals/
    └── features/
         ↓
    DuckDB Queries ←──── Both you & collaborator
    (zero-copy S3 read)
         ↓
   ML Features Table
         ↓
  XGBoost Classifier
  (value stock predictions)
```

### **Key Design Principles**

✅ **Hybrid S3 + Local**: Data in S3 (single source of truth), DuckDB queries it directly
✅ **Zero operations**: No servers, no Databricks, no complex orchestration
✅ **Collaboration-ready**: Share code + AWS creds, automatic data updates
✅ **Scalable**: Can move to Databricks later if needed (Parquet format compatible)
✅ **Cost-effective**: ~$1-2/month S3 storage + $100/month EODHD API

## 📦 **Repository Structure**

```
eodhd-pipeline/
├── ingestion/              # Data fetching from EODHD
│   ├── eodhd_client.py     # API wrapper with rate limiting
│   ├── ingest_prices.py    # EOD price data → S3 Parquet
│   ├── ingest_fundamentals.py  # Financial statements → S3 Parquet
│   └── utils.py            # Shared helpers
│
├── database/               # DuckDB setup
│   ├── schema.sql          # Table definitions (YOU CREATE THIS)
│   └── init_db.py          # Database initialization
│
├── features/               # Feature engineering (Phase 2)
│   ├── price_features.py   # Technical indicators
│   └── fundamental_features.py  # Financial ratios
│
├── models/                 # ML models (Phase 3)
│   ├── train_classifier.py # XGBoost training
│   └── predict.py          # Inference
│
├── analysis/               # SQL queries & notebooks
│   └── example_queries.sql # Sample DuckDB queries
│
├── config/                 # Configuration
│   ├── tickers.txt         # 1000 ticker list
│   └── settings.yaml       # Pipeline config
│
├── data/                   # Local data (gitignored)
│   └── stocks.duckdb       # Optional local DB
│
└── tests/                  # Unit tests
```

## 🚀 **Getting Started**

### **1. Setup Environment**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your EODHD API key and AWS credentials
```

### **2. Create S3 Bucket**

```bash
# Create bucket for data storage
aws s3 mb s3://your-bucket-name

# Update .env with bucket name
S3_BUCKET=your-bucket-name
```

### **3. Initial Data Ingestion (You'll Build This!)**

```bash
# Start with a small test (5 tickers, 1 year)
python ingestion/ingest_prices.py --tickers "AAPL,MSFT,GOOGL,AMZN,NVDA" --years 1

# Verify data in S3
aws s3 ls s3://your-bucket/stock-data/prices/ --recursive

# Query with DuckDB (from Python)
python -c "
import duckdb
conn = duckdb.connect()
conn.execute('INSTALL httpfs; LOAD httpfs;')
df = conn.execute(\"\"\"
    SELECT * FROM read_parquet('s3://your-bucket/stock-data/prices/**/*.parquet')
    WHERE symbol = 'AAPL' LIMIT 10
\"\"\").df()
print(df)
"
```

## 📚 **Learning Roadmap**

### **Phase 1: Price Data Ingestion (Week 1)**
**Goal**: Get EOD price data into S3 Parquet

**Tasks**:
1. Implement `eodhd_client.py`
   - Use EODHD ChatGPT to understand API endpoints
   - Add rate limiting (1000 req/min)
   - Handle errors and retries

2. Implement `ingest_prices.py`
   - Fetch data for 5 tickers, 1 year (test)
   - Convert to Polars DataFrame
   - Write to local Parquet first (debug easier)
   - Upload to S3 with partitioning

3. Test DuckDB queries
   - Query S3 Parquet directly
   - Verify data quality

4. Scale up
   - Add all 1000 tickers
   - Backfill 20 years
   - Add checkpointing (resume on failures)

**Resources**:
- EODHD API docs: https://eodhd.com/financial-apis/
- DuckDB S3 docs: https://duckdb.org/docs/guides/import/s3_import

### **Phase 2: Fundamentals & Features (Week 2-3)**
**Goal**: Add financial statements and engineer ML features

**Tasks**:
1. Implement `ingest_fundamentals.py`
   - Parse nested JSON from EODHD
   - Flatten to tabular format
   - Handle quarterly vs annual data

2. Create DuckDB schema
   - Write `database/schema.sql`
   - Define tables for prices, fundamentals, features

3. Feature engineering
   - Calculate financial ratios (P/E, P/B, ROE, etc.)
   - Add value signals (Piotroski score, etc.)
   - Handle point-in-time correctness (avoid lookahead bias!)

### **Phase 3: ML Model (Week 4+)**
**Goal**: Train XGBoost classifier for value investing

**Tasks**:
1. Define target variable (what is a "value stock"?)
2. Train model on historical features
3. Evaluate performance
4. Create inference script for daily predictions

## 💡 **Key Concepts to Learn**

### **1. DuckDB Zero-Copy S3 Queries**

DuckDB can query Parquet files in S3 without downloading them:

```python
import duckdb

conn = duckdb.connect(':memory:')
conn.execute("INSTALL httpfs; LOAD httpfs;")

# Set AWS credentials
conn.execute("SET s3_region='us-east-1';")
conn.execute("SET s3_access_key_id='...';")
conn.execute("SET s3_secret_access_key='...';")

# Query S3 directly!
df = conn.execute("""
    SELECT * FROM read_parquet('s3://bucket/prices/**/*.parquet')
    WHERE symbol = 'AAPL'
""").df()
```

### **2. Parquet Partitioning**

Organize files for efficient queries:

```
s3://bucket/stock-data/
├── prices/
│   ├── year=2024/month=01/AAPL.parquet
│   ├── year=2024/month=01/MSFT.parquet
│   └── year=2024/month=02/AAPL.parquet
└── fundamentals/
    └── statement_type=income/year=2024/AAPL.parquet
```

DuckDB pushes down filters → only reads relevant files!

### **3. Rate Limiting**

EODHD limits: 1000 req/min, 100k req/day

```python
from tenacity import retry, wait_fixed, stop_after_attempt
import time

@retry(wait=wait_fixed(0.06), stop=stop_after_attempt(3))
def fetch_with_rate_limit(url):
    # 0.06s = 1000 requests/minute
    time.sleep(0.06)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### **4. Point-in-Time Correctness**

Critical for ML: Don't use future data!

```python
# BAD: Using Q3 earnings for September predictions
# (Q3 earnings not reported until ~November)

# GOOD: Use Q2 earnings for September predictions
# (Q2 report available in August)
```

## 🤝 **Collaboration Workflow**

**Your workflow**:
```bash
# Ingest new data
python ingestion/ingest_prices.py --incremental  # Daily updates

# Data automatically goes to S3
# Your friend's queries automatically see new data!
```

**Your friend's workflow**:
```bash
# Clone repo
git clone <repo-url>

# Configure AWS creds in .env
# (Same S3 bucket access)

# Query data
python analysis/my_custom_analysis.py

# Or use DuckDB CLI
duckdb -c "
SELECT * FROM read_parquet('s3://bucket/prices/**/*.parquet')
WHERE symbol = 'AAPL'
"
```

No file sharing needed! S3 is single source of truth.

## 🎓 **Questions & Answers**

**Q: Why DuckDB instead of PostgreSQL/MySQL?**
A: DuckDB is columnar (fast analytics), embedded (no server), and has native Parquet/S3 support.

**Q: Why Parquet instead of CSV?**
A: 10x smaller files, columnar compression, schema enforcement, works seamlessly with DuckDB.

**Q: Can I still move to Databricks later?**
A: Yes! Parquet is standard format. Just point Databricks at your S3 bucket.

**Q: How much will 20GB in S3 cost?**
A: ~$0.50/month storage + negligible query costs (DuckDB is smart about data transfer).

**Q: What if I want faster local queries?**
A: Option 1: Materialize specific data to local DuckDB
  Option 2: Keep entire dataset local (20GB is manageable)
  Option 3: Hybrid (S3 for exploration, local for production models)

## 📖 **Next Steps**

1. **Now**: Review this README, explore folder structure
2. **Today**: Implement `eodhd_client.py` - get your first API call working
3. **This week**: Complete Phase 1 (price data ingestion)
4. **Ask questions**: I'm here to help when you get stuck!

## 🔗 **Resources**

- **EODHD API**: https://eodhd.com/financial-apis/
- **EODHD ChatGPT**: Use for API details and examples
- **DuckDB Docs**: https://duckdb.org/docs/
- **Polars Guide**: https://pola-rs.github.io/polars-book/
- **XGBoost Docs**: https://xgboost.readthedocs.io/

---

**Built for learning and collaboration** 🚀
Start simple, iterate, and scale when needed.
