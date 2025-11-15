import flask
from flask import request, jsonify, render_template
from services.file_upload.file_upload_handler import file_source_factory
from services.file_upload.file_processer import FileProcesser
app = flask.Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the application."""
    return jsonify({'status': 'running'}), 200

@app.route("/upload", methods=["POST"])
def upload():
    try:
        source = file_source_factory(request)
        file_bytes, filename, source_link = source.load()
        file_processer = FileProcesser()
        result = file_processer.process(file_bytes, filename)
        
        return jsonify({
            "status": "success",
            "filename": result["filename"],
            "file_type": result["file_type"],
            "extracted_text": result["raw_text"][:500],  # return first 500 chars
            "categories": result["categories"],
            "citation": source_link
        })

    except Exception as e:
        print(f"Error processing file: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/app', methods=['GET'])
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)