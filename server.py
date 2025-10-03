"""
OpenAI-Compatible Web Server
Hosts an API with OpenAI-compatible endpoints
"""

import os
from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from functools import wraps
from dotenv import load_dotenv
import time
import requests
import json

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_KEY = os.getenv('API_KEY', 'Nano')
CUSTOM_ENDPOINT_URL = os.getenv('CUSTOM_ENDPOINT_URL', '')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

# Provider API Keys (configure these in .env for actual API access)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
XAI_API_KEY = os.getenv('XAI_API_KEY', '')

# Sample models list - can be customized
AVAILABLE_MODELS = [
    {
        "id": "gpt-3.5-turbo",
        "object": "model",
        "created": 1677610602,
        "owned_by": "openai",
        "permission": [],
        "root": "gpt-3.5-turbo",
        "parent": None,
    },
    {
        "id": "gpt-4",
        "object": "model",
        "created": 1687882411,
        "owned_by": "openai",
        "permission": [],
        "root": "gpt-4",
        "parent": None,
    },
    {
        "id": "gpt-4-turbo-preview",
        "object": "model",
        "created": 1706037777,
        "owned_by": "openai",
        "permission": [],
        "root": "gpt-4-turbo-preview",
        "parent": None,
    },
]

# AI Providers configuration
AI_PROVIDERS = {
    'chatgpt': {
        'name': 'ChatGPT',
        'url': 'https://chat.openai.com',
        'check_endpoint': 'https://chat.openai.com/api/auth/session',
    },
    'claude': {
        'name': 'Claude',
        'url': 'https://claude.ai',
        'check_endpoint': 'https://claude.ai/api/auth/session',
    },
    'grok': {
        'name': 'Grok',
        'url': 'https://grok.x.ai',
        'check_endpoint': 'https://grok.x.ai/api/auth/session',
    },
    'gemini': {
        'name': 'Gemini',
        'url': 'https://gemini.google.com',
        'check_endpoint': 'https://gemini.google.com/api/auth/session',
    },
    'perplexity': {
        'name': 'Perplexity',
        'url': 'https://www.perplexity.ai',
        'check_endpoint': 'https://www.perplexity.ai/api/auth/session',
    },
    'copilot': {
        'name': 'Microsoft Copilot',
        'url': 'https://copilot.microsoft.com',
        'check_endpoint': 'https://copilot.microsoft.com/api/auth/session',
    },
}


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "error": {
                    "message": "Missing Authorization header",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_api_key"
                }
            }), 401
        
        # Expected format: "Bearer <API_KEY>"
        if not auth_header.startswith('Bearer '):
            return jsonify({
                "error": {
                    "message": "Invalid Authorization header format. Expected 'Bearer <API_KEY>'",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_api_key"
                }
            }), 401
        
        provided_key = auth_header[7:]  # Remove "Bearer " prefix
        
        if provided_key != API_KEY:
            return jsonify({
                "error": {
                    "message": "Invalid API key provided",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_api_key"
                }
            }), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


@app.route('/')
def index():
    """Root endpoint - basic info"""
    return jsonify({
        "message": "OpenAI-Compatible Web Server",
        "version": "1.0.0",
        "endpoints": {
            "models": "/v1/models",
            "chat_completions": "/v1/chat/completions",
            "access_panel": "/access"
        }
    })


@app.route('/access')
def access_panel():
    """AI Provider Access Panel - HTML interface"""
    return render_template('access.html')


@app.route('/api/providers/<provider_id>/status', methods=['GET'])
def check_provider_status(provider_id):
    """
    Check the status of an AI provider
    Returns whether the provider is accessible
    """
    if provider_id not in AI_PROVIDERS:
        return jsonify({
            "status": "error",
            "message": "Unknown provider"
        }), 404
    
    provider = AI_PROVIDERS[provider_id]
    
    # For now, we'll simulate checking by attempting to access the provider
    # In a real implementation, this would check if we can reach the provider
    # and potentially verify authentication status
    try:
        import requests
        # Simple check - just try to reach the main URL with a timeout
        response = requests.get(provider['url'], timeout=5, allow_redirects=True)
        
        if response.status_code < 500:
            return jsonify({
                "status": "working",
                "message": f"Provider is accessible",
                "provider": provider['name']
            })
        else:
            return jsonify({
                "status": "not-working",
                "message": f"Provider returned error {response.status_code}",
                "provider": provider['name']
            })
    except Exception as e:
        return jsonify({
            "status": "not-working",
            "message": f"Cannot reach provider: {str(e)}",
            "provider": provider['name']
        })


@app.route('/api/providers/<provider_id>/session', methods=['GET'])
def get_provider_session(provider_id):
    """
    Get session token for an AI provider
    This is a placeholder implementation - real session token retrieval
    would require browser automation or user authentication
    """
    if provider_id not in AI_PROVIDERS:
        return jsonify({
            "error": "Unknown provider"
        }), 404
    
    provider = AI_PROVIDERS[provider_id]
    
    # Note: This is a placeholder implementation
    # In a real-world scenario, you would need to:
    # 1. Use browser automation (e.g., Selenium, Playwright) to login
    # 2. Extract session cookies/tokens from the authenticated session
    # 3. Store and manage these tokens securely
    # 4. Handle token refresh when they expire
    
    return jsonify({
        "token": f"[PLACEHOLDER-TOKEN-{provider_id.upper()}-{int(time.time())}]",
        "message": "This is a placeholder token. Real implementation requires browser automation to extract actual session tokens.",
        "provider": provider['name'],
        "note": "Session token extraction requires user authentication and proper security measures"
    })


@app.route('/v1/models', methods=['GET'])
@require_api_key
def list_models():
    """
    List available models endpoint
    Compatible with OpenAI's GET /v1/models endpoint
    """
    return jsonify({
        "object": "list",
        "data": AVAILABLE_MODELS
    })


@app.route('/v1/models/<model_id>', methods=['GET'])
@require_api_key
def get_model(model_id):
    """
    Get specific model details
    Compatible with OpenAI's GET /v1/models/{model} endpoint
    """
    for model in AVAILABLE_MODELS:
        if model['id'] == model_id:
            return jsonify(model)
    
    return jsonify({
        "error": {
            "message": f"Model '{model_id}' not found",
            "type": "invalid_request_error",
            "param": None,
            "code": "model_not_found"
        }
    }), 404


@app.route('/v1/chat/completions', methods=['POST'])
@require_api_key
def chat_completions():
    """
    Chat completions endpoint
    Compatible with OpenAI's POST /v1/chat/completions endpoint
    Forwards requests to configured AI providers based on the model
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": {
                    "message": "Request body is required",
                    "type": "invalid_request_error",
                    "param": None,
                    "code": "invalid_request"
                }
            }), 400
        
        model = data.get('model')
        messages = data.get('messages', [])
        stream = data.get('stream', False)
        
        if not model:
            return jsonify({
                "error": {
                    "message": "Missing required parameter: 'model'",
                    "type": "invalid_request_error",
                    "param": "model",
                    "code": "missing_parameter"
                }
            }), 400
        
        if not messages:
            return jsonify({
                "error": {
                    "message": "Missing required parameter: 'messages'",
                    "type": "invalid_request_error",
                    "param": "messages",
                    "code": "missing_parameter"
                }
            }), 400
        
        # Route to appropriate provider based on model
        if model.startswith('gpt-') or model.startswith('o1-'):
            if not OPENAI_API_KEY:
                return jsonify({
                    "error": {
                        "message": "OpenAI API key not configured. Please set OPENAI_API_KEY in .env file",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "api_key_not_configured"
                    }
                }), 500
            
            return forward_to_openai(data, stream)
        
        elif model.startswith('claude-'):
            if not ANTHROPIC_API_KEY:
                return jsonify({
                    "error": {
                        "message": "Anthropic API key not configured. Please set ANTHROPIC_API_KEY in .env file",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "api_key_not_configured"
                    }
                }), 500
            
            return forward_to_anthropic(data, stream)
        
        elif model.startswith('gemini-'):
            if not GOOGLE_API_KEY:
                return jsonify({
                    "error": {
                        "message": "Google API key not configured. Please set GOOGLE_API_KEY in .env file",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "api_key_not_configured"
                    }
                }), 500
            
            return forward_to_google(data, stream)
        
        elif model.startswith('grok-'):
            if not XAI_API_KEY:
                return jsonify({
                    "error": {
                        "message": "xAI API key not configured. Please set XAI_API_KEY in .env file",
                        "type": "invalid_request_error",
                        "param": None,
                        "code": "api_key_not_configured"
                    }
                }), 500
            
            return forward_to_xai(data, stream)
        
        else:
            return jsonify({
                "error": {
                    "message": f"Model '{model}' is not supported",
                    "type": "invalid_request_error",
                    "param": "model",
                    "code": "model_not_supported"
                }
            }), 400
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": f"Internal server error: {str(e)}",
                "type": "server_error",
                "param": None,
                "code": "internal_error"
            }
        }), 500


def forward_to_openai(data, stream):
    """Forward request to OpenAI API"""
    try:
        headers = {
            'Authorization': f'Bearer {OPENAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            stream=stream
        )
        
        if stream:
            def generate():
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            
            return Response(
                stream_with_context(generate()),
                content_type=response.headers.get('content-type', 'text/event-stream')
            )
        else:
            return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": f"Error forwarding to OpenAI: {str(e)}",
                "type": "server_error",
                "param": None,
                "code": "forwarding_error"
            }
        }), 500


def forward_to_anthropic(data, stream):
    """Forward request to Anthropic API (Claude)"""
    try:
        # Convert OpenAI format to Anthropic format
        messages = data.get('messages', [])
        anthropic_messages = []
        system_message = None
        
        for msg in messages:
            if msg['role'] == 'system':
                system_message = msg['content']
            else:
                anthropic_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
        
        anthropic_data = {
            'model': data.get('model', 'claude-3-5-sonnet-20241022'),
            'messages': anthropic_messages,
            'max_tokens': data.get('max_tokens', 4096),
            'stream': stream
        }
        
        if system_message:
            anthropic_data['system'] = system_message
        
        if 'temperature' in data:
            anthropic_data['temperature'] = data['temperature']
        
        headers = {
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=anthropic_data,
            stream=stream
        )
        
        if stream:
            def generate():
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            
            return Response(
                stream_with_context(generate()),
                content_type=response.headers.get('content-type', 'text/event-stream')
            )
        else:
            # Convert Anthropic response to OpenAI format
            anthropic_response = response.json()
            
            openai_response = {
                "id": f"chatcmpl-{anthropic_response.get('id', '')}",
                "object": "chat.completion",
                "created": int(time.time()),
                "model": data.get('model'),
                "choices": [{
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": anthropic_response.get('content', [{}])[0].get('text', '')
                    },
                    "finish_reason": anthropic_response.get('stop_reason', 'stop')
                }],
                "usage": {
                    "prompt_tokens": anthropic_response.get('usage', {}).get('input_tokens', 0),
                    "completion_tokens": anthropic_response.get('usage', {}).get('output_tokens', 0),
                    "total_tokens": anthropic_response.get('usage', {}).get('input_tokens', 0) + anthropic_response.get('usage', {}).get('output_tokens', 0)
                }
            }
            
            return jsonify(openai_response), response.status_code
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": f"Error forwarding to Anthropic: {str(e)}",
                "type": "server_error",
                "param": None,
                "code": "forwarding_error"
            }
        }), 500


def forward_to_google(data, stream):
    """Forward request to Google Gemini API"""
    try:
        # Convert OpenAI format to Gemini format
        messages = data.get('messages', [])
        gemini_contents = []
        
        for msg in messages:
            role = 'user' if msg['role'] in ['user', 'system'] else 'model'
            gemini_contents.append({
                'role': role,
                'parts': [{'text': msg['content']}]
            })
        
        model_name = data.get('model', 'gemini-pro')
        
        gemini_data = {
            'contents': gemini_contents,
        }
        
        if 'temperature' in data:
            gemini_data['generationConfig'] = {'temperature': data['temperature']}
        
        # Gemini API uses URL parameters for API key
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent'
        params = {'key': GOOGLE_API_KEY}
        
        response = requests.post(
            url,
            params=params,
            json=gemini_data
        )
        
        if response.status_code != 200:
            return jsonify(response.json()), response.status_code
        
        # Convert Gemini response to OpenAI format
        gemini_response = response.json()
        
        content = ''
        if 'candidates' in gemini_response and len(gemini_response['candidates']) > 0:
            candidate = gemini_response['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content']:
                content = candidate['content']['parts'][0].get('text', '')
        
        openai_response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": data.get('model'),
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": content
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
        
        return jsonify(openai_response), 200
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": f"Error forwarding to Google: {str(e)}",
                "type": "server_error",
                "param": None,
                "code": "forwarding_error"
            }
        }), 500


def forward_to_xai(data, stream):
    """Forward request to xAI (Grok) API"""
    try:
        # xAI uses OpenAI-compatible API
        headers = {
            'Authorization': f'Bearer {XAI_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            'https://api.x.ai/v1/chat/completions',
            headers=headers,
            json=data,
            stream=stream
        )
        
        if stream:
            def generate():
                for chunk in response.iter_content(chunk_size=None):
                    if chunk:
                        yield chunk
            
            return Response(
                stream_with_context(generate()),
                content_type=response.headers.get('content-type', 'text/event-stream')
            )
        else:
            return jsonify(response.json()), response.status_code
    
    except Exception as e:
        return jsonify({
            "error": {
                "message": f"Error forwarding to xAI: {str(e)}",
                "type": "server_error",
                "param": None,
                "code": "forwarding_error"
            }
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": {
            "message": "Endpoint not found",
            "type": "invalid_request_error",
            "param": None,
            "code": "not_found"
        }
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": {
            "message": "Internal server error",
            "type": "server_error",
            "param": None,
            "code": "internal_error"
        }
    }), 500


if __name__ == '__main__':
    print(f"Starting OpenAI-Compatible Web Server...")
    print(f"API Key: {API_KEY}")
    print(f"Host: {HOST}")
    print(f"Port: {PORT}")
    if CUSTOM_ENDPOINT_URL:
        print(f"Custom Endpoint URL: {CUSTOM_ENDPOINT_URL}")
    print(f"\nServer is running. Use Ctrl+C to stop.")
    
    app.run(host=HOST, port=PORT, debug=False)
