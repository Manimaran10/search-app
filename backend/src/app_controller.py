import flask
from flask import request, jsonify, render_template
from backend.src.services.file_upload.file_upload_handler import file_source_factory

app = flask.Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the application."""
    return jsonify({'status': 'running'}), 200

@app.route("/upload", methods=["POST"])
def upload():
    try:
        source = file_source_factory(request)
        file_bytes, filename = source.load()

        with open(f"/tmp/{filename}", "wb") as f:
            f.write(file_bytes)

        return jsonify({"status": "success", "filename": filename})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/app', methods=['GET'])
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)