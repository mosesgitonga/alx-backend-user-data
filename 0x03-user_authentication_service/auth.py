#!/usr/bin/env python3.10
"""
User authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _generate_uuid(self) -> str:
    """
    return a string representation of a new uuid
    """
    uuid = str(uuid4())
    return uuid


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate login
        Args:
            email -> email of the user
            password -> password to validate
        Return:
            returns a boolean
        """
        try:
            existing_user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = existing_user.hashed_password

        if bcrypt.checkpw(password.encode('utf-8'), user_password):
            return True
        else:
            return False
