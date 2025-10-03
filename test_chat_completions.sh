#!/bin/bash
# Test script for chat completions endpoint

echo "=========================================="
echo "Testing Chat Completions Endpoint"
echo "=========================================="
echo ""

# Base URL
BASE_URL="http://localhost:5000"
API_KEY="Nano"

echo "1. Testing chat completions with OpenAI model (without API key configured)..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "2. Testing chat completions with Claude model (without API key configured)..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "3. Testing chat completions with Gemini model (without API key configured)..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-pro",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "4. Testing chat completions with Grok model (without API key configured)..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-beta",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "5. Testing chat completions with missing model parameter..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "6. Testing chat completions with missing messages parameter..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo"
  }' | python -m json.tool
echo ""
echo ""

echo "7. Testing chat completions with unsupported model..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "unsupported-model-123",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "8. Testing chat completions without authentication..."
curl -s $BASE_URL/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "Hello!"}]
  }' | python -m json.tool
echo ""
echo ""

echo "=========================================="
echo "All tests completed!"
echo "=========================================="
