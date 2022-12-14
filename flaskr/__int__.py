import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from config import DevelopmentConfig
from .models import setup_db
from .users import all_users

load_dotenv()
message = os.environ.get('MESSAGE', 'I could not find any message')

def create_app(config=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    setup_db(app)

    @app.route('/')
    def index():
        return jsonify({"message": message})

    @app.route('/users/')
    def _all_users():
        return all_users()

    return app
