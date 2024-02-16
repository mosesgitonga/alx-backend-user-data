#!/usr/bin/env python3
"""
session authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4
import os


class SessionAuth(Auth):
    """
    session authentication mechanism
    """
    user_id_by_session_id = {}

    def __init__(self):
        pass

    def create_session(self, user_id: str = None) -> str:
        """
        creating a session and storing the user_id a session
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        returns user_id by  getting userid from the dictionary attribute
        """
        if session_id is None and not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id, None)
        return user_id

    def current_user(self, request=None):
        """
        returns the user id of the current user
        """
        # Retrieve the value of the _my_session_id cookie from the request
        session_id = self.session_cookie(request)
        # Look up the corresponding User ID based on the session_id
        user_id = self.user_id_for_session_id(session_id)
        # Retrieve the User instance from the database based on the user_id
        user = User.get(user_id)
        # Return the User instance
        return user


if __name__ == '__main__':
    session_auth = SessionAuth()
    print(session_auth)
