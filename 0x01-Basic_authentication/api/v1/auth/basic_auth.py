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
        """
        decoding base64
        """
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

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        get the user credentials
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        username, password = decoded_base64_authorization_header.split(':', 1)
        return username, password


    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on his
        email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            found_users = User.search({'email': user_email})
        except Exception:
            return None

        for user in found_users:
            if user.is_valid_password(user_pwd):
                return user

        return None
