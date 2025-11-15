import flask
from flask import Blueprint, request, jsonify, render_template
from flask.views import MethodView

app = flask.Flask(__name__)


@app.route('/status', methods=['GET'])
def status():
    """Endpoint to check the status of the application."""
    return jsonify({'status': 'running'}), 200


@app.route('/app', methods=['GET'])
def index():
    return render_template("index.html")



if __name__ == '__main__':
    app.run(debug=True)