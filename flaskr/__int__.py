from flask import Flask, jsonify

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({"Choo Choo": "Welcome to your Flask app"})

    return app