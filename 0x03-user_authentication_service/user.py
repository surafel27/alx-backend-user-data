#!/usr/bin/env python3
"""
This module defines a SQLAlchemy data model for representing user data.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from typing import Optional


Base = declarative_base()


class User(Base):
    """
    Represents a user in the application.

    Attributes:
        id (int): Primary key identifying the user.
        email (str): Email address of the user. Cannot be null.
        hashed_password (str): Hashed password of the user. Cannot be null.
        session_id (str): Session ID of the user. Can be null.
        reset_token (str): Token used for password reset. Can be null.
    """
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250))
    reset_token: Optional[str] = Column(String(250))
