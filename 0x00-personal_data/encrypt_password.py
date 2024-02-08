#!/usr/bin/env python3
"""
encryoting password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """salting password for security purpose
    """
    password_bytes = password.encode('utf-8')

    salt = bcrypt.gensalt()

    hashed_passwd = bcrypt.hashpw(password_bytes, salt)

    return hashed_passwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validating password
    """
    password_bytes = password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_password)
