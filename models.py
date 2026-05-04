from pydantic import BaseModel


class SentimentResponse(BaseModel):
    product_id: int
    latest_sentiment_score: float
    rolling_average_sentiment: float

    class Config:
        from_attributes = True
