import flask
from flask import request, jsonify, render_template,send_from_directory, Flask
from flask_cors import CORS
from services.file_upload.file_upload_handler import file_source_factory
from services.file_upload.file_processer import FileProcesser
from services.searcher.query_service import QueryService
import logging
import os
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))              # backend/
BUILD_DIR = os.path.join(BASE_DIR, "../../frontend/build")           # absolute path
print("React build dir:", BUILD_DIR)

app = Flask(__name__, static_folder=BUILD_DIR, static_url_path="/")
CORS(app, 
     origins=["http://localhost:3000", "http://127.0.0.1:3000"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)
# ---------- Serve React ----------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    file_path = os.path.join(BUILD_DIR, path)

    # If the file exists, return it
    if path != "" and os.path.exists(file_path):
        return send_from_directory(BUILD_DIR, path)

    # Otherwise return index.html
    return send_from_directory(BUILD_DIR, "index.html")
    
@app.before_request
def log_request():
    print("REQUEST:", request.method, request.path)


@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the application."""
    return jsonify({'status': 'running'}), 200

@app.route("/api/upload", methods=["POST"])
def upload():
    try:
        source = file_source_factory(request)
        file_bytes, filename, source_link = source.load()
        file_processer = FileProcesser()
        result = file_processer.process(file_bytes, source_link)
        if not result:
            raise Exception("File processing failed")
        return jsonify({
            "status": "file uploaded successfully",
            "data": result
        }), 200

    except Exception as e:
        logger.error(f"File upload failed: {e}", exc_info=True)
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    
@app.route('/api/query', methods=['POST'])
def query():
    try:
        query_json = request.json
        query_text = query_json.get('q', None)
        filters = query_json.get('filters', {})
        do_hybrid_search = query_json.get('hybrid', True)
        if not query_text:
            return jsonify({
                "status": "error",
                "message": "Query parameter 'q' is required"
            }), 400
        query_service = QueryService()

        results = query_service.query(query_text, query_filters=filters, do_hybrid_search=do_hybrid_search)

        return jsonify({
            "status": "success",
            "data": {
                "results": results if results else [],
                "total": len(results) if results else 0
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/app', methods=['GET'])
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)