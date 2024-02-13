#!/usr/bin/env python3
""" Main 2
"""
from flask import Flask, request
from api.v1.auth.basic_auth import BasicAuth

app = Flask(__name__)
a = BasicAuth()

with app.app_context():
    print(a.extract_base64_authorization_header(None))
    print(a.extract_base64_authorization_header(89))
    print(a.extract_base64_authorization_header("Holberton School"))
    print(a.extract_base64_authorization_header("Basic Holberton"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9u"))
    print(a.extract_base64_authorization_header("Basic SG9sYmVydG9uIFNjaG9vbA=="))
    print(a.extract_base64_authorization_header("Basic1234"))