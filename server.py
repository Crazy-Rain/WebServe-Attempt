"""
OpenAI-Compatible Web Server
Hosts an API with OpenAI-compatible endpoints
"""

import os
from flask import Flask, request, jsonify
from functools import wraps
from dotenv import load_dotenv

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
            "models": "/v1/models"
        }
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
