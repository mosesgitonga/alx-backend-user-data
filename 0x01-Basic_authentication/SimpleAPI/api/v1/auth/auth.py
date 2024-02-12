#!/usr/bin/env python3
from typing import List, TypeVar
from flask import request


class Auth():
    """
    authentication class
    """
    def __init__(self):
        pass
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        authentcation request
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        header for authorization
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user 
        """
        return None