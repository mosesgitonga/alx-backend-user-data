#!/usr/bin/env python3
"""
Basic authentication
"""
#from api.v1.auth.auth import Auth
from flask import request
import base64


class BasicAuth:
    """
    basic authentication class
    """
    def __init__(self):
        pass

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        extracting authorization hearder
        """

        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None

        if authorization_header.startswith('Basic '):
           value_after_Basic = authorization_header[6:]
           return value_after_Basic
        else:
            return None

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            if decoded_bytes:
                return decoded_bytes.decode('utf-8')
            else:
                return False
        except Exception:
            pass