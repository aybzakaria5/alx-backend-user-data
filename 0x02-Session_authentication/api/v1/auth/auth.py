#!/usr/bin/env python3
""" to manage the API authentication.
"""

from flask import request
from typing import List, TypeVar


class Auth:
    """
    Template for all authentication system you will implement.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Check if authentication is required for the given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths
            that are excluded from authentication.

        Returns:
            bool: True if authentication is required
            False otherwise.
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
        """
        Returns the authorization header for the given request.

        Args:
            request (Optional): The request object. Defaults to None.

        Returns:
            str: The authorization header.
        """
        if request is None:
            return None
        if 'Authorization' in request.headers:
            return request.headers['Authorization']
        else:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieve the current authenticated user.

        Args:
            request (Optional[Request]):
            The request object representing
            the current HTTP request.

        Returns:
            User: The current authenticated user.

        """
        return None
