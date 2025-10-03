# Usage Example

## Starting the Server

```bash
$ python server.py
Starting OpenAI-Compatible Web Server...
API Key: Nano
Host: 0.0.0.0
Port: 5000
Custom Endpoint URL: http://localhost:5000

Server is running. Use Ctrl+C to stop.
 * Serving Flask app 'server'
 * Debug mode: off
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
```

## Example API Calls

### 1. List All Models

```bash
$ curl http://localhost:5000/v1/models \
  -H "Authorization: Bearer Nano"
```

**Response:**
```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-3.5-turbo",
      "object": "model",
      "created": 1677610602,
      "owned_by": "openai",
      "permission": [],
      "root": "gpt-3.5-turbo",
      "parent": null
    },
    {
      "id": "gpt-4",
      "object": "model",
      "created": 1687882411,
      "owned_by": "openai",
      "permission": [],
      "root": "gpt-4",
      "parent": null
    },
    {
      "id": "gpt-4-turbo-preview",
      "object": "model",
      "created": 1706037777,
      "owned_by": "openai",
      "permission": [],
      "root": "gpt-4-turbo-preview",
      "parent": null
    }
  ]
}
```

### 2. Get Specific Model

```bash
$ curl http://localhost:5000/v1/models/gpt-4 \
  -H "Authorization: Bearer Nano"
```

**Response:**
```json
{
  "id": "gpt-4",
  "object": "model",
  "created": 1687882411,
  "owned_by": "openai",
  "permission": [],
  "root": "gpt-4",
  "parent": null
}
```

### 3. Chat Completions with OpenAI Models

**Important:** To use this endpoint, you must configure the appropriate provider API key in your `.env` file.

```bash
$ curl http://localhost:5000/v1/chat/completions \
  -H "Authorization: Bearer Nano" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "What is the capital of France?"}
    ]
  }'
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "The capital of France is Paris."
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 25,
    "completion_tokens": 8,
    "total_tokens": 33
  }
}
```

**Without API key configured:**
```json
{
  "error": {
    "code": "api_key_not_configured",
    "message": "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file",
    "param": null,
    "type": "invalid_request_error"
  }
}
```

### 4. Chat Completions with Claude

```bash
$ curl http://localhost:5000/v1/chat/completions \
  -H "Authorization: Bearer Nano" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [
      {"role": "user", "content": "Explain quantum computing in simple terms."}
    ]
  }'
```

The server automatically converts between OpenAI and Anthropic formats, so you always use the same request format regardless of the provider.

### 5. Chat Completions with Gemini

```bash
$ curl http://localhost:5000/v1/chat/completions \
  -H "Authorization: Bearer Nano" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-pro",
    "messages": [
      {"role": "user", "content": "What are the benefits of renewable energy?"}
    ]
  }'
```

### 6. Using with Python OpenAI Library

```python
import openai

# Configure the client to use your custom server
openai.api_key = "Nano"
openai.api_base = "http://localhost:5000/v1"

# List models
models = openai.Model.list()
print(models)

# Chat completion (requires provider API key configured on server)
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
print(response.choices[0].message.content)

# You can also use Claude models with the same interface
response = openai.ChatCompletion.create(
    model="claude-3-5-sonnet-20241022",
    messages=[
        {"role": "user", "content": "Explain machine learning."}
    ]
)
print(response.choices[0].message.content)
```

### 7. Using with JavaScript/TypeScript

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'Nano',
  baseURL: 'http://localhost:5000/v1',
});

// List models
const models = await openai.models.list();
console.log(models);

// Chat completion (requires provider API key configured on server)
const completion = await openai.chat.completions.create({
  model: 'gpt-3.5-turbo',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' }
  ],
});
console.log(completion.choices[0].message.content);

// You can also use Claude or Gemini models with the same interface
const claudeCompletion = await openai.chat.completions.create({
  model: 'claude-3-5-sonnet-20241022',
  messages: [
    { role: 'user', content: 'Explain neural networks.' }
  ],
});
console.log(claudeCompletion.choices[0].message.content);
```

## Customizing Configuration

Edit the `.env` file to customize:

```env
# Server API key (for authenticating client requests to your server)
API_KEY=MySecretKey123

# Custom port
PORT=8080

# Custom host
HOST=127.0.0.1

# Custom endpoint URL (optional)
CUSTOM_ENDPOINT_URL=http://myserver:8080

# AI Provider API Keys (required for actual model serving)
OPENAI_API_KEY=sk-...  # Your OpenAI API key
ANTHROPIC_API_KEY=sk-ant-...  # Your Anthropic API key
GOOGLE_API_KEY=...  # Your Google API key
XAI_API_KEY=...  # Your xAI API key
```

Then restart the server to apply changes.

**Note:** You only need to configure the provider API keys for the services you want to use. The server will provide helpful error messages if you try to use a model from an unconfigured provider.
