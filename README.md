# WebServe-Attempt

An OpenAI-compatible web server that hosts an API connection with customizable API key and endpoints.

## Features

- 🔑 API Key authentication (default: "Nano", customizable)
- 🔌 OpenAI-compatible endpoints
- 📋 List available models via `/v1/models` endpoint
- 🤖 AI Provider Access Panel for monitoring multiple AI chat interfaces
- 🟢 Real-time status indicators for AI providers (ChatGPT, Claude, Grok, Gemini, etc.)
- 🔐 Session token management for web-based AI providers
- ⚙️ Configurable base URL and port
- 🚀 Easy to set up and use

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

- `API_KEY`: The API key required for authentication (default: "Nano")
- `CUSTOM_ENDPOINT_URL`: Custom base URL for the endpoint (optional)
- `PORT`: Port number to run the server on (default: 5000)
- `HOST`: Host address to bind to (default: 0.0.0.0)

## Using with OpenAI-Compatible Clients

This server is compatible with any client that supports custom OpenAI endpoints. For example:

**Python (openai library):**
```python
import openai

openai.api_key = "Nano"
openai.api_base = "http://localhost:5000/v1"

models = openai.Model.list()
print(models)
```

**JavaScript/TypeScript:**
```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'Nano',
  baseURL: 'http://localhost:5000/v1',
});

const models = await openai.models.list();
console.log(models);
```

## License

See LICENSE file for details.
