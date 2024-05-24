#!/usr/bin/env python3
"""a file to manage API authentication"""

from flask import request
from typing import List, TypeVar


class Auth:
    """ a template ckass for all aythentication
    system
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Method to determine if authentication is required
        Currently, always returns False.
        :param path: string path to be checked
        :param excluded_paths: list of string paths that
        are excluded from authentication
        :return: False or True
        """
        if path is None:
            return True
        if not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and excluded_path == path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from
        the request , now it returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        a method to get the current user from the request
        now it returns NOne
        """
        return None
