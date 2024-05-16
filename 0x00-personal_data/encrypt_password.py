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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Return True if the provided password matches i
    the hashed password; otherwise, return False."""
    # Convert the password string to bytes
    password_bytes = password.encode()

    # Use bcrypt to verify if the provided password matches the hashed password
    return bcrypt.checkpw(password_bytes, hashed_password)
