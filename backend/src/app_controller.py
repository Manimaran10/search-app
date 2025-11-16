import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flask
from flask import request, jsonify, render_template
from services.file_upload.file_upload_handler import file_source_factory
from services.file_upload.file_processer import FileProcesser
from services.searcher.query_service import QueryService
import logging
app = flask.Flask(__name__)
logger = logging.getLogger(__name__)

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
    app.run(debug=True)