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
def logout() -> str:
    """
    logout
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    session_id = request.cookies.get('session_id', None)

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    response = jsonify({'email': user.email})
    return response, 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    email = request.form['email']

    if not email:
        abort(403)

    token = AUTH.get_reset_password_token(email)
    response = jsonify({"email": email, "reset_token": token})
    return response, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
