#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify
from auth import Auth
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """
    returns simple message
    """
    return jsonify({"message": "Bienvenue"})

@app.route('/users/<email>/<password>', methods=['POST'])
def register_user(email, passowrd):
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
