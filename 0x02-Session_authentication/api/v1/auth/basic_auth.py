#!/usr/bin/env python3
"""
define BasicAuth class
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    represents a basic authentication mechanism that extends the
    abstract Auth class.
    """
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Extract the credentials from the 'Authorization' header.
        """
        if authorization_header is None:
            return None

        if not type(authorization_header) is str:
            return None

        if not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header[6:]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decode base64-encoded credentials from the 'Authorization' header.
        """
        if base64_authorization_header is None:
            return None

        if not type(base64_authorization_header) is str:
            return None

        try:
            credentials = base64_authorization_header
            decoded_credentials = base64.b64decode(credentials).decode('utf-8')
            return decoded_credentials
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> (str, str):
        """
        Extract user credentials from a decoded Base64-encoded
        'Authorization' header.
        """
        if not decoded_base64_authorization_header:
            return (None, None)

        if not type(decoded_base64_authorization_header) is str:
            return (None, None)

        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        else:
            separated = decoded_base64_authorization_header.split(':', 1)
            return tuple(separated)

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Return the User instance based on the given email and password.
        """
        if (user_email is None or type(user_email) is not str
                or user_pwd is None or type(user_pwd) is not str):
            return None

        user = User()
        matching_users = user.search(attributes={'email': user_email})

        if not matching_users:
            return None

        for user in matching_users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current User based on the request's 'Authorization' header.
        """
        auth_header = self.authorization_header(request)
        extract = self.extract_base64_authorization_header(auth_header)
        decode = self.decode_base64_authorization_header(extract)
        email, pwd = self.extract_user_credentials(decode)
        user = self.user_object_from_credentials(email, pwd)
        return user
