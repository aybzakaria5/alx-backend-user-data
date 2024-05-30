#!/usr/bin/env python3
"""hashing passwords and adding salt to it"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generates a new UUID and returns it as a string"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash the password
        hashed_password = _hash_password(password)

        # Add user to the database
        user = self._db.add_user(email, hashed_password)

        return user

    def create_session(self, email: str) -> str:
        """Create a session for the user identified by the given email"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def valid_login(self, email: str, password: str) -> bool:
        """checkgin if the login is valid"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False
    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from a session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
