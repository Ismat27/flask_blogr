import os
from flask import Flask, jsonify
from dotenv import load_dotenv

load_dotenv()
message = os.environ.get('MESSAGE', 'I could not find any message')

def create_app(test_config=None):
    app = Flask(__name__)

    @app.route('/')
    def index():
        return jsonify({"message": message})

    return app