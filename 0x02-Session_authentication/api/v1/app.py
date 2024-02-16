#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = os.getenv('AUTH_TYPE')

if auth_type == "basic_auth":
    auth = BasicAuth()
elif auth_type == 'auth':
    auth = Auth()
elif auth_type == 'session_auth':
    auth = SessionAuth()


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    handler for forbiden page
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorized page
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.before_request
def user_authorization():
    """user authentication
    """
    if auth is None:
        return
    # Create list of excluded paths
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']
    # if request.path is not part of the list above, do nothing
    # You must use the method require_auth from the auth instance
    if not auth.require_auth(request.path, excluded_paths):
        return
    # If auth.authorization_header(request) and auth.session_cookie(request)
    # return None, raise the error, 401 - you must use abort

    if auth.authorization_header(request) is None \
            and auth.session_cookie(request) is None:
        return None, abort(401)


    auth_header = auth.authorization_header(request)

    # If auth.current_user(request) returns None, raise the error 403 - you
    # must use abort
    user = auth.current_user(request)
    if user is None:
        abort(403)

    request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
