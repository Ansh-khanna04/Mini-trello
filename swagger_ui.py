"""
Swagger UI Integration for Mini Trello Flask App
Serves the OpenAPI specification with interactive documentation
"""

import os
import yaml
from flask import Blueprint, render_template_string, jsonify, current_app

swagger_bp = Blueprint('swagger', __name__, url_prefix='/api-docs')


def load_api_spec():
    """Load the OpenAPI specification from YAML or JSON file."""
    import json
    
    # Try loading YAML first - find project root correctly
    # The Flask app root_path might be in 'app' subdirectory, so we need to find project root
    app_root = current_app.root_path
    
    # If we're in an 'app' subdirectory, go up one level
    if os.path.basename(app_root) == 'app':
        project_root = os.path.dirname(app_root)
    else:
        project_root = app_root
    
    yaml_path = os.path.join(project_root, 'docs', 'api-spec-corrected.yaml')
    json_path = os.path.join(project_root, 'docs', 'api-spec-simple.json')
    
    print(f"[Swagger Debug] App root: {app_root}")
    print(f"[Swagger Debug] Project root: {project_root}")
    print(f"[Swagger Debug] YAML path: {yaml_path}")
    print(f"[Swagger Debug] YAML exists: {os.path.exists(yaml_path)}")
    
    # First try YAML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as file:
            content = file.read()
            spec = yaml.safe_load(content)
            
            # Ensure required OpenAPI fields are present
            if not isinstance(spec, dict):
                raise ValueError("Invalid API specification format")
            
            if 'openapi' not in spec:
                spec['openapi'] = '3.0.0'
            
            if 'info' not in spec:
                spec['info'] = {'title': 'Mini Trello API', 'version': '1.0.0'}
            
            return spec
            
    except Exception as yaml_error:
        # If YAML fails, try JSON backup
        try:
            with open(json_path, 'r', encoding='utf-8') as file:
                spec = json.load(file)
                return spec
        except Exception as json_error:
            # If both fail, return minimal valid spec
            return {
                "openapi": "3.0.0",
                "info": {
                    "title": "Mini Trello API",
                    "version": "1.0.0",
                    "description": "API documentation temporarily unavailable"
                },
                "paths": {},
                "error": f"YAML error: {yaml_error}, JSON error: {json_error}"
            }


@swagger_bp.route('/')
def swagger_ui():
    """Serve the Swagger UI interface."""
    swagger_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Trello API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui.css" />
    <link rel="icon" type="image/png" href="https://unpkg.com/swagger-ui-dist@5.10.5/favicon-32x32.png" sizes="32x32" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin:0;
            background: #fafafa;
        }
        .swagger-ui .topbar {
            background-color: #0079bf;
        }
        .swagger-ui .topbar .download-url-wrapper {
            display: none;
        }
        #loading {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-family: Arial, sans-serif;
            font-size: 18px;
            color: #0079bf;
        }
    </style>
</head>
<body>
    <div id="loading">Loading API Documentation...</div>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@5.10.5/swagger-ui-standalone-preset.js"></script>
    <script>
        console.log('Initializing Swagger UI...');
        
        // First, fetch the spec to check if it's valid
        fetch('/api-docs/spec.json')
        .then(response => {
            console.log('Spec response status:', response.status);
            return response.json();
        })
        .then(spec => {
            console.log('Spec loaded:', spec);
            console.log('Paths found:', Object.keys(spec.paths || {}).length);
            
            // Hide loading message
            document.getElementById('loading').style.display = 'none';
            
            // Initialize Swagger UI
            const ui = SwaggerUIBundle({
                spec: spec,  // Use the fetched spec directly
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout",
                validatorUrl: null,
                docExpansion: "list",
                operationsSorter: "alpha",
                tagsSorter: "alpha",
                filter: true,
                tryItOutEnabled: true,
                requestInterceptor: function(req) {
                    console.log('API Request:', req.method, req.url);
                    if (!req.headers['Content-Type'] && req.method !== 'GET') {
                        req.headers['Content-Type'] = 'application/json';
                    }
                    return req;
                },
                responseInterceptor: function(res) {
                    console.log('API Response:', res.status, res.url);
                    return res;
                },
                onComplete: function() {
                    console.log('Swagger UI initialized successfully');
                },
                onFailure: function(err) {
                    console.error('Swagger UI initialization failed:', err);
                    document.getElementById('swagger-ui').innerHTML = 
                        '<div style="padding: 20px; text-align: center; color: #d32f2f;">' +
                        '<h2>Failed to load API documentation</h2>' +
                        '<p>Error: ' + err.message + '</p>' +
                        '</div>';
                }
            });
            
            window.ui = ui;
        })
        .catch(err => {
            console.error('Failed to fetch spec:', err);
            document.getElementById('loading').style.display = 'none';
            document.getElementById('swagger-ui').innerHTML = 
                '<div style="padding: 20px; text-align: center; color: #d32f2f;">' +
                '<h2>Failed to load API specification</h2>' +
                '<p>Error: ' + err.message + '</p>' +
                '<p><a href="/api-docs/spec.json">View raw spec</a> | <a href="/api-docs/debug">Debug info</a></p>' +
                '</div>';
        });
    </script>
</body>
</html>
    """
    return render_template_string(swagger_html)


@swagger_bp.route('/spec.json')
def api_spec():
    """Serve the OpenAPI specification as JSON."""
    spec = load_api_spec()
    
    # Update the server URL to match the current request
    from flask import request
    base_url = f"{request.scheme}://{request.host}"
    
    if 'servers' in spec and isinstance(spec['servers'], list):
        # Update the first server to match current host
        spec['servers'][0]['url'] = base_url
        if len(spec['servers']) > 1:
            spec['servers'] = [spec['servers'][0]]  # Keep only current server
    
    return jsonify(spec)


@swagger_bp.route('/debug')
def debug_spec():
    """Debug endpoint to check spec loading."""
    spec = load_api_spec()
    return jsonify({
        'spec_keys': list(spec.keys()) if isinstance(spec, dict) else 'NOT_DICT',
        'openapi_version': spec.get('openapi', 'MISSING'),
        'info_version': spec.get('info', {}).get('version', 'MISSING') if isinstance(spec.get('info'), dict) else 'INFO_NOT_DICT',
        'has_paths': 'paths' in spec,
        'error': spec.get('error', None)
    })


@swagger_bp.route('/redoc')
def redoc():
    """Serve ReDoc documentation (alternative to Swagger UI)."""
    redoc_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Mini Trello API Documentation</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>
        body { margin: 0; padding: 0; }
    </style>
</head>
<body>
    <redoc spec-url='/api-docs/spec.json'></redoc>
    <script src="https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js"> </script>
</body>
</html>
    """
    return render_template_string(redoc_html)


# Helper function to register the blueprint
def init_swagger_ui(app):
    """Initialize Swagger UI with the Flask app."""
    app.register_blueprint(swagger_bp)
    
    @app.route('/docs')
    def docs_redirect():
        """Redirect /docs to the Swagger UI."""
        from flask import redirect, url_for
        return redirect(url_for('swagger.swagger_ui'))
    
    print("📚 API Documentation available at:")
    print("  - Swagger UI: http://localhost:5000/api-docs/")
    print("  - ReDoc:      http://localhost:5000/api-docs/redoc")
    print("  - JSON Spec:  http://localhost:5000/api-docs/spec.json")
    print("  - Debug Info: http://localhost:5000/api-docs/debug")
    print("  - Quick Link: http://localhost:5000/docs")
