#!/usr/bin/env python3
""" handeling the api authentication
"""

from flask import request
from typing import List, TypeVar
import os


class Auth:
    """
    class fpr auth blueprint
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.
        """
        if path is None or excluded_paths is None:
            return True
        elif len(excluded_paths) == 0:
            return True

        path = path.rstrip('/')
        for i in excluded_paths:
            stripped = i.rstrip('/')
            if path == stripped:
                return False
        if path in excluded_paths:
            return False
        if i[-1] == "*":
            if path.startswith(i[:-1]):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ check the authorization header
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user
        """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request
        """
        if request is None:
            return None
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
