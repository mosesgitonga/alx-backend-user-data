#!/usr/bin/env python3.10
"""
User authentication
"""
import bcrypt
from db import DB
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registering a new user into the db
        Args:
            email -> email of the new user
            password -> password of the new user
        return:
            returns the user object
        """
        db = self._db._session
        existing_user = db.query(User).filter_by(email=email).first()

        if existing_user:
            raise ValueError('User {} already exists'.format(email))

        password = _hash_password(password)
        self._db.add_user(email, password)


def _hash_password(password: str) -> bytes:
    """
    hashes a passwrd by adding some salt :)
    args:
        password -> password to be hashed
    return:
        bytes -> hashed password
    """
    passwd_bytes = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(passwd_bytes, bcrypt.gensalt())
    return hashed_password
