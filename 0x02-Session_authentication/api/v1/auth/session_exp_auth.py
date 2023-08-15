#!/usr/bin/env python3
""" Module of Session Expiration
"""

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for handling session-based authentication
    with expiration.
    """

    def __init__(self):
        """
        Initialize a SessionExpAuth instance and assign session_duration
        from environment variable.
        """
        duration_str = os.environ.get('SESSION_DURATION')
        try:
            self.session_duration = int(duration_str) if duration_str else 0
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Create a new session for the specified user ID.
        The generated session ID can be used for managing user sessions.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
                "user_id": user_id,
                "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a given session ID,
        considering session expiration.
        """
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        if self.session_duration <= 0:
            return self.user_id_by_session_id.get(session_id).get("user_id")
        if not self.user_id_by_session_id.get(session_id).get("created_at"):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        created_at = session_dict.get("created_at")
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None
        return self.user_id_by_session_id.get(session_id).get("user_id")
