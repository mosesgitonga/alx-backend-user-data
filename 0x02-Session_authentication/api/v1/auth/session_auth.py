#!/usr/bin/env python3
"""
session authentication
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    def __init__(self):
        pass

if __name__ == '__main__':
    session_auth = SessionAuth()
    print(session_auth)