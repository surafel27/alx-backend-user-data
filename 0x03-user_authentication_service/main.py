#!/usr/bin/env python3

"""
test the API endpoint
"""
import requests


BASE_URL = "http://localhost:5000"


def register_user(email: str, password: str) -> None:
    """
    Test registration of a new user.
    """
    response = requests.post(
        f"{BASE_URL}/users",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """
    Test login with a wrong password.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 401


def profile_unlogged() -> None:
    """
    Test accessing the profile while unlogged.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """
    Test successful login.
    """
    response = requests.post(
        f"{BASE_URL}/sessions",
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    return response.cookies.get("session_id")


def profile_logged(session_id: str) -> None:
    """
    Test accessing the profile while logged in
    """
    response = requests.get(
        f"{BASE_URL}/profile",
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200


def log_out(session_id: str) -> None:
    """
    Test user logout.
    """
    response = requests.delete(
        f"{BASE_URL}/sessions",
        cookies={"session_id": session_id}
    )
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """
    Test getting a reset password token
    """
    response = requests.post(
        f"{BASE_URL}/reset_password",
        data={"email": email}
    )
    assert response.status_code == 200
    return response.json()["reset_token"]


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """
    Test updating a user's password using a reset token.
    """
    response = requests.put(
        f"{BASE_URL}/reset_password",
        data={"email": email, "reset_token": reset_token,
              "new_password": new_password}
    )
    assert response.status_code == 200


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
