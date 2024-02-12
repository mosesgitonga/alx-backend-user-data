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

        if path is None:
            return True
        
        if excluded_paths is None or excluded_paths == []:
            return True
        
        
        normalized_path = path.rstrip('/')
        
        # Check if the normalized path is in the list of excluded paths
        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_path == normalized_excluded_path:
                return False

        return True
        
        

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