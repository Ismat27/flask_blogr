from flask import jsonify
from .models import User

def all_users():
    users = User.query.all()
    users = [
        user.format() for
        user in users
    ]
    return jsonify(users)