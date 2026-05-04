import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import Depends, FastAPI, Header, HTTPException, status

from models import SentimentResponse

ROOT = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    db_path = ROOT / "reviews_db.sqlite"
    connection = sqlite3.connect(str(db_path), check_same_thread=False)
    connection.row_factory = sqlite3.Row
    app.state.db = connection
    yield
    connection.close()


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health_check():
    try:
        db_connection = app.state.db
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        if result and result[0] == 1:
            return {
                "status": "healthy",
                "database": "connected",
                "code": 200,
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"DB connection error: {str(e)}",
        ) from e


API_KEY_SECRET = os.getenv("API_KEY", "my-secret-key")


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key. Access Denied.",
        )
    return x_api_key


@app.get("/api/v1/sentiment/{product_id}", response_model=SentimentResponse)
def get_sentiment(product_id: int, key: str = Depends(verify_api_key)):
    db = app.state.db
    cursor = db.cursor()

    query = """
        SELECT prod_id, rating, rolling_average_sentiment
        FROM Analytical_Sentiment
        WHERE prod_id = ?
        ORDER BY review_id DESC LIMIT 1
        """
    cursor.execute(query, (product_id,))
    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Product ID not found")

    return {
        "product_id": row["prod_id"],
        "latest_sentiment_score": row["rating"],
        "rolling_average_sentiment": row["rolling_average_sentiment"],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
