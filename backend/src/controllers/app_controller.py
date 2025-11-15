import flask
from flask import Blueprint, request, jsonify
from flask.views import MethodView
from flask_cors import CORS
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import requests

app = flask.Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Mock database for files and search results
uploaded_files = []
search_database = [
    {
        "id": 1,
        "content": "Sample Response about AI automation in marketing workflows",
        "categories": {
            "topic": "automation",
            "project": "Hey Amigo",
            "team": "Marketing",
            "citation": "https://example.com/marketing-ai"
        }
    },
    {
        "id": 2,
        "content": "Documentation on SEO optimization techniques using AI tools",
        "categories": {
            "topic": "seo",
            "project": "Hey Amigo", 
            "team": "SEO",
            "citation": "https://example.com/seo-guide"
        }
    },
    {
        "id": 3,
        "content": "Development best practices for implementing AI agents",
        "categories": {
            "topic": "development",
            "project": "Hey Amigo",
            "team": "Development",
            "citation": "https://example.com/dev-practices"
        }
    }
]

class AppController(MethodView):
    """Controller for application-related endpoints."""

    def get(self):
        """Handle GET requests to retrieve application info."""
        app_info = {
            'name': 'AI Knowledge Base',
            'version': '1.0.0',
            'description': 'AI-powered search and knowledge management system'
        }
        return jsonify(app_info), 200

def status():
    """Endpoint to check the status of the application."""
    return jsonify({'status': 'running'}), 200

@app.route('/api/search', methods=['GET'])
def search():
    """Search endpoint for knowledge base."""
    query = request.args.get('q', '').lower()
    
    if not query:
        return jsonify({'results': []}), 200
    
    # Simple search implementation - filter by content or categories
    results = []
    for item in search_database:
        if (query in item['content'].lower() or 
            query in item['categories']['topic'].lower() or
            query in item['categories']['team'].lower() or
            query in item['categories']['project'].lower()):
            results.append(item)
    
    return jsonify({'results': results}), 200

@app.route('/api/files', methods=['GET'])
def get_files():
    """Get list of uploaded files."""
    return jsonify({'files': uploaded_files}), 200

@app.route('/api/upload', methods=['POST'])
def upload_files():
    """Handle file uploads (local files and URLs)."""
    try:
        # Handle local file uploads
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    
                    # Get file stats
                    file_stats = os.stat(file_path)
                    file_size = file_stats.st_size
                    
                    # Add to uploaded files list
                    file_info = {
                        'id': len(uploaded_files) + 1,
                        'name': filename,
                        'size': format_file_size(file_size),
                        'uploadDate': datetime.now().strftime('%b %d, %Y'),
                        'type': filename.split('.')[-1].lower() if '.' in filename else 'unknown',
                        'downloads': 0,
                        'path': file_path
                    }
                    uploaded_files.append(file_info)
        
        # Handle URL uploads
        public_url = request.form.get('publicUrl')
        if public_url:
            try:
                # Download file from URL
                response = requests.get(public_url, stream=True)
                if response.status_code == 200:
                    # Extract filename from URL
                    filename = public_url.split('/')[-1]
                    if not filename or '.' not in filename:
                        filename = f"url_file_{len(uploaded_files) + 1}.txt"
                    
                    filename = secure_filename(filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    
                    # Get file stats
                    file_stats = os.stat(file_path)
                    file_size = file_stats.st_size
                    
                    # Add to uploaded files list
                    file_info = {
                        'id': len(uploaded_files) + 1,
                        'name': filename,
                        'size': format_file_size(file_size),
                        'uploadDate': datetime.now().strftime('%b %d, %Y'),
                        'type': filename.split('.')[-1].lower() if '.' in filename else 'unknown',
                        'downloads': 0,
                        'path': file_path,
                        'source_url': public_url
                    }
                    uploaded_files.append(file_info)
            except Exception as e:
                return jsonify({'error': f'Failed to download file from URL: {str(e)}'}), 400
        
        return jsonify({'message': 'Files uploaded successfully', 'files': uploaded_files}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 Bytes"
    
    size_names = ["Bytes", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"

# Register the routes
app.add_url_rule('/app', view_func=AppController.as_view('app_controller'))

# Create a separate route for status
@app.route('/status', methods=['GET'])
def status_endpoint():
    """Status endpoint."""
    return jsonify({'status': 'running'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)