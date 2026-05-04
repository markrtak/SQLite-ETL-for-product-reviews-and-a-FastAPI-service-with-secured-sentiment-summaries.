#!/bin/bash

BASE_URL="http://127.0.0.1:8000"
API_KEY="my-secret-key"
PRODUCT_ID=101

echo "-----------------------------------------------"
echo "Testing Health Endpoint..."
curl -X GET "$BASE_URL/health"
echo -e "\n"

echo "-----------------------------------------------"
echo "Testing Secured Sentiment Endpoint (Product $PRODUCT_ID)..."
curl -i -X GET "$BASE_URL/api/v1/sentiment/$PRODUCT_ID" \
     -H "X-API-Key: $API_KEY" \
     -H "accept: application/json"
echo -e "\n"

echo "-----------------------------------------------"
echo "Testing Security (Sending WRONG Key)..."
curl -i -X GET "$BASE_URL/api/v1/sentiment/$PRODUCT_ID" \
     -H "X-API-Key: wrong-key-123"
echo "-----------------------------------------------"
