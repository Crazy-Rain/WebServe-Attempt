# WebServe-Attempt

An OpenAI-compatible web server that hosts an API connection with customizable API key and endpoints.

## Features

- 🔑 API Key authentication (default: "Nano", customizable)
- 🔌 OpenAI-compatible endpoints
- 💬 Chat completions endpoint that forwards requests to real AI providers
- 📋 List available models via `/v1/models` endpoint
- 🤖 AI Provider Access Panel for monitoring multiple AI chat interfaces
- 🟢 Real-time status indicators for AI providers (ChatGPT, Claude, Grok, Gemini, etc.)
- 🔐 Session token management for web-based AI providers
- ⚙️ Configurable base URL and port
- 🚀 Easy to set up and use
- 🌐 Support for multiple AI providers: OpenAI, Anthropic (Claude), Google (Gemini), xAI (Grok)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

3. (Optional) Customize your configuration in `.env`:
```
API_KEY=Nano
CUSTOM_ENDPOINT_URL=http://localhost:5000
PORT=5000
HOST=0.0.0.0
```

4. **Configure AI Provider API Keys (Required for actual model serving):**

To enable actual AI model serving, you need to configure API keys for the providers you want to use. Add these to your `.env` file:

```
# OpenAI (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (for Claude models)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google (for Gemini models)
GOOGLE_API_KEY=your_google_api_key_here

# xAI (for Grok models)
XAI_API_KEY=your_xai_api_key_here
```

Get your API keys from:
- OpenAI: https://platform.openai.com/api-keys
- Anthropic: https://console.anthropic.com/
- Google: https://makersuite.google.com/app/apikey
- xAI: https://console.x.ai/

**Note:** You only need to configure API keys for the providers you want to use. The server will work without them, but will return error messages when trying to use models from unconfigured providers.

## Usage

### Start the Server

```bash
python server.py
```

The server will start on `http://0.0.0.0:5000` by default.

### Quick Test

To test the server, you can use the provided test script:

```bash
# Start the server in one terminal
python server.py

# In another terminal, run the test script
./test_server.sh
```

### API Endpoints

#### GET `/access`
Access the AI Provider Access Panel - a web interface for monitoring and managing connections to AI chat services.

**Access via browser:**
```
http://localhost:5000/access
```

This panel provides:
- Real-time status monitoring for multiple AI providers (ChatGPT, Claude, Grok, Gemini, Perplexity, Microsoft Copilot)
- Visual status indicators (🟢 green = working, 🔴 red = not accessible, 🟠 orange = checking)
- Session token retrieval for web-based authentication
- Easy-to-use interface for managing AI provider connections

#### POST `/v1/chat/completions`
Send chat completion requests to AI models. This endpoint is compatible with OpenAI's chat completions API and forwards requests to the appropriate AI provider based on the model specified.

**Supported Models:**
- **OpenAI models**: `gpt-3.5-turbo`, `gpt-4`, `gpt-4-turbo-preview`, `o1-preview`, `o1-mini`, etc.
- **Anthropic models**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, etc.
- **Google models**: `gemini-pro`, `gemini-1.5-pro`, etc.
- **xAI models**: `grok-beta`, etc.

**Request:**
```bash
curl http://localhost:5000/v1/chat/completions \
  -H "Authorization: Bearer Nano" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-3.5-turbo",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
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
      "content": "Hello! How can I assist you today?"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

**With Claude:**
```bash
curl http://localhost:5000/v1/chat/completions \
  -H "Authorization: Bearer Nano" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-3-5-sonnet-20241022",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

**Note:** You must configure the appropriate provider API key in your `.env` file for the model you want to use. If the API key is not configured, you'll receive an error message with instructions.

#### GET `/v1/models`
List all available models on the server.

**Request:**
```bash
curl http://localhost:5000/v1/models \
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
    ...
  ]
}
```

#### GET `/v1/models/{model_id}`
Get details about a specific model.

**Request:**
```bash
curl http://localhost:5000/v1/models/gpt-4 \
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

#### GET `/api/providers/{provider_id}/status`
Check the status of a specific AI provider.

**Request:**
```bash
curl http://localhost:5000/api/providers/chatgpt/status
```

**Response:**
```json
{
  "status": "working",
  "message": "Provider is accessible",
  "provider": "ChatGPT"
}
```

**Available Providers:** `chatgpt`, `claude`, `grok`, `gemini`, `perplexity`, `copilot`

#### GET `/api/providers/{provider_id}/session`
Get session token for a specific AI provider.

**Request:**
```bash
curl http://localhost:5000/api/providers/chatgpt/session
```

**Response:**
```json
{
  "token": "[SESSION-TOKEN]",
  "message": "Token retrieved successfully",
  "provider": "ChatGPT"
}
```

**Note:** Session token extraction requires browser automation and user authentication in a production environment. The current implementation provides placeholder tokens for demonstration purposes.

## Authentication

All API endpoints (except `/access` and provider endpoints) require API key authentication using the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

The default API key is `Nano`, but you can customize it in the `.env` file.

## Configuration

The server can be configured using environment variables in the `.env` file:

### Server Configuration
- `API_KEY`: The API key required for authentication (default: "Nano")
- `CUSTOM_ENDPOINT_URL`: Custom base URL for the endpoint (optional)
- `PORT`: Port number to run the server on (default: 5000)
- `HOST`: Host address to bind to (default: 0.0.0.0)

### AI Provider API Keys
Configure these to enable actual model serving:
- `OPENAI_API_KEY`: Your OpenAI API key (for GPT models)
- `ANTHROPIC_API_KEY`: Your Anthropic API key (for Claude models)
- `GOOGLE_API_KEY`: Your Google API key (for Gemini models)
- `XAI_API_KEY`: Your xAI API key (for Grok models)

See the installation section for where to obtain these API keys.

## Using with OpenAI-Compatible Clients

This server is compatible with any client that supports custom OpenAI endpoints. For example:

**Python (openai library):**
```python
import openai

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
```

**JavaScript/TypeScript:**
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
```

**Note:** The server acts as a proxy, forwarding requests to the actual AI providers. You need to configure the appropriate provider API keys on the server (in the `.env` file) for the models you want to use.

## License

See LICENSE file for details.
