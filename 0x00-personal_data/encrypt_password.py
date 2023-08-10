#!/usr/bin/env python3
"""
hash a password to never see the plain text
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    salted and hashed password will be returned, which is a byte string
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Compair Validates and checks a password against the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
