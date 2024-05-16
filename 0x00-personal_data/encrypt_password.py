#!/usr/bin/env python3
"""encrypting passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return a salted, hashed password using bcrypt."""
    # Convert the password string to bytes
    password_bytes = password.encode()

    # Generate a salted, hashed password using bcrypt
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password
