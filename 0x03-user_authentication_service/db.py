#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a user to the database and return the User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **kwargs):
        """finding a user """
        try:
            # Query the users table based on the input keyword arguments
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                # If no user found, raise NoResultFound
                raise NoResultFound("No user found for the given criteria")

            return user
        except NoResultFound as e:
            # Catch and re-raise NoResultFound
            raise e
        except InvalidRequestError as e:
            # Catch and re-raise InvalidRequestError
            raise e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes and commit changes to the database"""
        # Find the user by user_id
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            # If no user found, raise ValueError
            raise ValueError(f"No user found with id {user_id}")

        # Update the user's attributes based on the provided keyword arguments
        for key, value in kwargs.items():
            if hasattr(User, key):
                setattr(user, key, value)
            else:
                # If an invalid attribute is provided, raise ValueError
                raise ValueError(f"Invalid attribute '{key}'")

        # Commit changes to the database
        self._session.commit()
