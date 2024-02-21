#!/usr/bin/env python3.10
"""
User authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


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
        try:
            existing_user = self._db.find_user_by(email=email)

            if existing_user is not None:
                raise ValueError('User {} already exists'.format(email))
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)


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
