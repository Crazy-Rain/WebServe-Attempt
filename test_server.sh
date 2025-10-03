#!/bin/bash
# Test script for the OpenAI-compatible web server

echo "=========================================="
echo "Testing OpenAI-Compatible Web Server"
echo "=========================================="
echo ""

# Base URL
BASE_URL="http://localhost:5000"
API_KEY="Nano"

echo "1. Testing root endpoint..."
curl -s $BASE_URL | python -m json.tool
echo ""
echo ""

echo "2. Testing /v1/models without authentication (should fail)..."
curl -s $BASE_URL/v1/models | python -m json.tool
echo ""
echo ""

echo "3. Testing /v1/models with wrong API key (should fail)..."
curl -s $BASE_URL/v1/models -H "Authorization: Bearer WrongKey" | python -m json.tool
echo ""
echo ""

echo "4. Testing /v1/models with correct API key (should succeed)..."
curl -s $BASE_URL/v1/models -H "Authorization: Bearer $API_KEY" | python -m json.tool
echo ""
echo ""

echo "5. Testing /v1/models/gpt-4 (should succeed)..."
curl -s $BASE_URL/v1/models/gpt-4 -H "Authorization: Bearer $API_KEY" | python -m json.tool
echo ""
echo ""

echo "6. Testing /v1/models/nonexistent (should return 404)..."
curl -s $BASE_URL/v1/models/nonexistent -H "Authorization: Bearer $API_KEY" | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
