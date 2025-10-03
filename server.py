"""
OpenAI-Compatible Web Server
Hosts an API with OpenAI-compatible endpoints
"""

import os
from flask import Flask, request, jsonify, render_template
from functools import wraps
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
API_KEY = os.getenv('API_KEY', 'Nano')
CUSTOM_ENDPOINT_URL = os.getenv('CUSTOM_ENDPOINT_URL', '')
PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', '0.0.0.0')

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
