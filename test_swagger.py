#!/usr/bin/env python3
"""
Test script to check Swagger API spec endpoint
"""

import sys
import json
from flask import Flask
from swagger_ui import init_swagger_ui

# Create a minimal Flask app
app = Flask(__name__)

# Initialize Swagger UI
init_swagger_ui(app)

def test_spec_endpoint():
    """Test the /api-docs/spec.json endpoint"""
    with app.app_context():
        with app.test_client() as client:
            # Test the spec.json endpoint
            response = client.get('/api-docs/spec.json')
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    spec = response.get_json()
                    print(f"Spec loaded successfully!")
                    print(f"OpenAPI Version: {spec.get('openapi')}")
                    print(f"Title: {spec.get('info', {}).get('title')}")
                    print(f"Paths found: {len(spec.get('paths', {}))}")
                    
                    if spec.get('paths'):
                        print("First few paths:")
                        for i, path in enumerate(list(spec['paths'].keys())[:5]):
                            methods = list(spec['paths'][path].keys())
                            print(f"  {i+1}. {path} - Methods: {methods}")
                    else:
                        print("No paths found in spec!")
                        
                    # Check for errors
                    if 'error' in spec:
                        print(f"Error in spec: {spec['error']}")
                        
                except Exception as e:
                    print(f"Error parsing JSON response: {e}")
                    print(f"Response content: {response.get_data(as_text=True)[:500]}...")
            else:
                print(f"Failed to get spec: {response.get_data(as_text=True)}")

if __name__ == '__main__':
    test_spec_endpoint()