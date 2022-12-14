from flask import Flask, jsonify
import os
from flaskr.__int__ import create_app
from dotenv import load_dotenv
from config import ProductionConfig

load_dotenv()

app = create_app(config=ProductionConfig)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
