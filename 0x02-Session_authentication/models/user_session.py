#!/usr/bin/env python3
""" UserSession module
"""
from models.base import Base


class UserSession(Base):
    """
    UserSession class represents a model to manage user sessions.

    This class inherits from the Base class and serves as a data model
    to store user session information.
    """
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize a new UserSession instance.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
