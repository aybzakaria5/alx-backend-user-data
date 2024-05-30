#!/usr/bin/env python3
"""hashing passwords and adding salt to it"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
