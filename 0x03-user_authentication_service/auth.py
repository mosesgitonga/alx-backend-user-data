#!/usr/bin/env python3.10
"""
User authentication
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _generate_uuid() -> str:
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

    def create_session(self, email: str) -> str:
        """
        creates a session id for a user
        Args:
            email -> is used to find a user
        Return:
            returns a string session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = str(uuid4())
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """
        retrieve user from the session id
        Args:
            session_id (str) -> will be used to search for the user
        Return:
            Union(user, None)
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroy a session
        Args:
            user_id (int) -> help to search for user
        Return:
            returns None
        """
        user = self._db.find_user_by(id=user_id)
        if user:
            user.session_id = None
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generate the reset_token
        Args:
            email -> used to find user
        Return:
            token string
        """
        try:
            user = self._db.find_user_by(email=email)
            token = str(uuid4())
            user.reset_token = token
            return user.reset_token
        except ValueError:
            raise ValueError

    def update_user(self, reset_token: str, password: str) -> None:
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except ValueError:
            raise ValueError

        hashed_password = _hash_password(password)
        user.hashed_password = hashed_password
        user.reset_token = None
