import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent

df = pd.read_csv(ROOT / "data" / "reviews.csv")


def csv_cleaning():
    df["comment"] = df["comment"].str.replace(r"\s+", " ", regex=True)

    df.dropna(subset=["rating", "comment", "prod_id"], inplace=True)
    df["cust_id"] = df["cust_id"].fillna("Anonymous")

    df["comment"] = df["comment"].str.strip().str.lower()


csv_cleaning()


db_path = ROOT / "reviews_db.sqlite"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Review;")
cursor.execute("DROP TABLE IF EXISTS Product;")
cursor.execute("DROP TABLE IF EXISTS Customer;")
cursor.execute("DROP TABLE IF EXISTS Analytical_Sentiment;")

with open(ROOT / "schema.sql", "r") as f:
    cursor.executescript(f.read())

customers = df[["cust_id"]].drop_duplicates()
products = df[["prod_id"]].drop_duplicates()

customers.to_sql("Customer", conn, if_exists="append", index=False)
products.to_sql("Product", conn, if_exists="append", index=False)
df.to_sql("Review", conn, if_exists="append", index=False)

query = """
    CREATE TABLE Analytical_Sentiment AS
    SELECT
        review_id,
        prod_id,
        rating,
        comment,
        AVG(rating) OVER (
            PARTITION BY prod_id
            ORDER BY review_id
            ROWS BETWEEN 4 PRECEDING AND CURRENT ROW
        ) AS rolling_average_sentiment
    FROM Review;
    """
cursor.execute(query)

conn.commit()
conn.close()
