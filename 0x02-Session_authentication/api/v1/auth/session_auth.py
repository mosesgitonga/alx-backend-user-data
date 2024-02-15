#!/usr/bin/env python3
"""
session authentication
"""
from auth import Auth


class SessionAuth(Auth):
    def __init__(self):
        pass

if __name__ == '__main__':
    session_auth = SessionAuth()
    print(session_auth)