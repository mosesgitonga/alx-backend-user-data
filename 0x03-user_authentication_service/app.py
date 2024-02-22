#!/usr/bin/env python3
"""
flask app
"""
from flask import Flask, jsonify, abort, request, redirect, url_for
from auth import Auth
from db import DB
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """
    returns simple message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    route to register new user
    """
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'])
def login():
    try:
        email = request.form['email']
        password = request.form['password']
    except KeyError as e:
        abort(400)

    valid = AUTH.valid_login(email, password)
    if valid is False:
        abort(401)

    session_id = AUTH.create_session(email)

    response = jsonify(email=email, message='logged in')
    response.set_cookie('session_id', session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    logout
    """
    try:
        session_id = request.cookies.get('session_id')
        if not session_id:
            raise KeyError('session id not found in cookies')
    except KeyError as e:
        abort(400)

    user = db.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(session_id)
        return redirect(url_for('index'))
    else:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
