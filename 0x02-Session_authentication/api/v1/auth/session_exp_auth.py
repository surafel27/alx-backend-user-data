#!/usr/bin/env python3
"""
SessionDBAuth Module
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class inherits from SessionExpAuth.

    It represents a session-based authentication mechanism
    for managing user sessions and access to protected resources,
    using a database to store user session information.
    """

    def create_session(self, user_id=None) -> str:
        """
        Create a new session for the specified user ID and store
        it in the database.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            "user_id": user_id,
            "session_id": session_id,
        }

        UserSession(**session_dict).save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a given session ID
        from the database.
        """

        if session_id is None:
            return None

        user_session = UserSession()
        user_session = user_session.search({'session_id': session_id})

        if not user_session:
            return None

        user_session = user_session[0]
        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy the user session associated with the given request.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        user_session = user_session[0]
        user_session.remove()

        del self.user_id_by_session_id[session_id]
        return True
