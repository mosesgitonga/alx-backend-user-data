#!/usr/bin/env python3.10
"""
User authentication
"""
import bcrypt

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
