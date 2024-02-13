#!/usr/bin/env python3
"""
Basic authentication
"""
from api.v1.auth.auth import Auth
from flask import request


class BasicAuth(Auth):
    """
    basic authentication class
    """
    def __init__(self):
        pass

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        extracting authorization hearder
        """
        authorization_header = request.header.get('Base64')

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if authorization_header.startwith('Basic '):
           value_after_Basic = authorization_header[7:]
           return value_after_Basic
        else:
            return None
