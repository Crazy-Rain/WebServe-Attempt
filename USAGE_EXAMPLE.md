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

### 3. Using with Python OpenAI Library

```python
import openai

# Configure the client to use your custom server
openai.api_key = "Nano"
openai.api_base = "http://localhost:5000/v1"

# List models
models = openai.Model.list()
print(models)
```

### 4. Using with JavaScript/TypeScript

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({
  apiKey: 'Nano',
  baseURL: 'http://localhost:5000/v1',
});

const models = await openai.models.list();
console.log(models);
```

## Customizing Configuration

Edit the `.env` file to customize:

```env
# Custom API key
API_KEY=MySecretKey123

# Custom port
PORT=8080

# Custom host
HOST=127.0.0.1

# Custom endpoint URL (optional)
CUSTOM_ENDPOINT_URL=http://myserver:8080
```

Then restart the server to apply changes.
