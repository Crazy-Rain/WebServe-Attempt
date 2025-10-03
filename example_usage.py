#!/usr/bin/env python3
"""
Example usage of the OpenAI-compatible server.
This demonstrates how to use the server with various clients.
"""

# Example 1: Using with curl (shown in comments)
# curl http://localhost:5000/v1/chat/completions \
#   -H "Authorization: Bearer Nano" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Hello!"}]
#   }'

# Example 2: Using with Python requests library
import requests
import json

def test_chat_completion():
    """Test the chat completions endpoint"""
    url = "http://localhost:5000/v1/chat/completions"
    headers = {
        "Authorization": "Bearer Nano",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is 2+2?"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    print("Status Code:", response.status_code)
    print("Response:", json.dumps(response.json(), indent=2))

def test_list_models():
    """Test the models endpoint"""
    url = "http://localhost:5000/v1/models"
    headers = {
        "Authorization": "Bearer Nano"
    }
    
    response = requests.get(url, headers=headers)
    print("Status Code:", response.status_code)
    print("Available Models:", json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("=" * 50)
    print("Testing List Models Endpoint")
    print("=" * 50)
    test_list_models()
    print("\n")
    
    print("=" * 50)
    print("Testing Chat Completions Endpoint")
    print("=" * 50)
    test_chat_completion()
    print("\n")
    
    print("Note: To actually use the chat completions endpoint,")
    print("configure the appropriate API keys in your .env file:")
    print("  OPENAI_API_KEY=your_key_here")
    print("  ANTHROPIC_API_KEY=your_key_here")
    print("  GOOGLE_API_KEY=your_key_here")
    print("  XAI_API_KEY=your_key_here")
