#!/usr/bin/env python3
"""Module for session authenticating views.
"""
import os
from typing import Tuple

from flask import abort, jsonify, request


from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_auth_login():
    """
    session authentication login
    """
    email = request.form.get('email')
    password = request.form.get('password')
    # If email is missing, return a JSON response with the status code 400
    if email is None:
        return jsonify({"error": "email missing"}), 400
    
    # If password is missing, return a JSON response with the status code 400
    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        found_users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if found_users:
        user = found_users[0]
    else:
        return jsonify({"error": "no user found for this email"}), 404

    for user in found_users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    user = found_users[0]
    
    from api.v1.app import auth

    SESSION_NAME = os.getenv('SESSION_NAME')
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)
    return response, 200

    
    
@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def session_auth_logout():
    """DELETE /api/v1/auth_session/logout

    Returns:
        - An empty JSON object.
    """
    from api.v1.app import auth
    # You must use auth.destroy_session(request) for deleting the Session ID
    is_destroyed = auth.destroy_session(request)
    # If destroy_session returns False, abort(404)
    if not is_destroyed:
        abort(404)
    # Otherwise, return an empty JSON dictionary with the status code 200
    return jsonify({}), 200
