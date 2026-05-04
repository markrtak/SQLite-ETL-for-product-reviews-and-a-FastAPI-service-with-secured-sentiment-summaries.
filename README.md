# Reviews sentiment API

SQLite ETL for product reviews and a FastAPI service with secured sentiment summaries.

End-to-end mini pipeline: relational schema loads into SQLite via an ETL script, then a secured FastAPI app exposes review sentiment aggregates per product.

Repository: [markrtak/SQLite-ETL-for-product-reviews-and-a-FastAPI-service-with-secured-sentiment-summaries.](https://github.com/markrtak/SQLite-ETL-for-product-reviews-and-a-FastAPI-service-with-secured-sentiment-summaries.)

## Layout

| Path | Purpose |
|------|---------|
| `schema.sql` | Creates `Customer`, `Product`, and `Review` tables. |
| `data/reviews.csv` | Source data for ETL. |
| `etl_pipeline.py` | Cleans CSV, builds `reviews_db.sqlite`, creates `Analytical_Sentiment` (rolling averages). |
| `app.py` | FastAPI app (health check + keyed sentiment endpoint). |
| `models.py` | Pydantic response model. |
| `scripts/curl_test.sh` | Sample `curl` calls (run from Git Bash or WSL). |

Generated `reviews_db.sqlite` is listed in `.gitignore`; build it locally before serving the API.

## Prerequisites

- Python 3.10+ recommended  
- Dependencies: `pip install pandas fastapi uvicorn pydantic`

## Usage

Run all commands from this directory (`reviews-sentiment-api`).

### 1. Build the database

```bash
python etl_pipeline.py
```

Creates `reviews_db.sqlite` in the project root.

### 2. Run the API

Optional: override the demo API key (default is `my-secret-key`).

```bash
# PowerShell example
$env:API_KEY = "your-secret-key"
python app.py
```

The app listens on `http://0.0.0.0:8000`. Alternatively:

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 3. Smoke-test

Use `scripts/curl_test.sh`, or manually:

```text
GET  http://127.0.0.1:8000/health
GET  http://127.0.0.1:8000/api/v1/sentiment/101  (header X-API-Key)
```
