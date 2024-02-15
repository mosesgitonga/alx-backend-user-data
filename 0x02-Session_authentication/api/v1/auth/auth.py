#!/usr/bin/env python3
"""
contains class for authentication
"""
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

        if path is None:
            return True
        
        if excluded_paths is ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/'] or excluded_paths == []:
            return True

        normalized_path = path.rstrip('/')
        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_path == normalized_excluded_path:
                return False

        return True
        
        
    def authorization_header(self, request=None) -> str:
        """
        header for authorization
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user 
        """
        return None
