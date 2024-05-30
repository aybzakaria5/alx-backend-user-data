#!/usr/bin/env python3
"""main module"""
import requests

BASE_URL = "http://localhost:5000"

def register_user(email_address: str, user_password: str) -> None:
    """
    Register a new user with the given email address and password.

    Args:
        email_address (str): The email address of the user.
        user_password (str): The password for the user.

    Returns:
        None
    """
    response = requests.post(f"{BASE_URL}/users", data={"email": email_address, "password": user_password})
    assert response.status_code == 200, f"Failed to register user: {response.text}"
    print("User registered successfully.")

def log_in_wrong_password(email_address: str, user_password: str) -> None:
    """
    Attempt to log in with an incorrect password.

    Args:
        email_address (str): The email address of the user.
        user_password (str): The incorrect password.

    Returns:
        None
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email_address, "password": user_password})
    assert response.status_code == 401, "Expected status code 401 for wrong password."
    print("Login with wrong password failed as expected.")

def log_in(email_address: str, user_password: str) -> str:
    """
    Log in the user with the given email address and password.

    Args:
        email_address (str): The email address of the user.
        user_password (str): The password for the user.

    Returns:
        str: The session ID received upon successful login.
    """
    response = requests.post(f"{BASE_URL}/sessions", data={"email": email_address, "password": user_password})
    assert response.status_code == 200, f"Failed to log in: {response.text}"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "No session ID received."
    print("Logged in successfully.")
    return session_id

def access_unlogged_profile() -> None:
    """
    Attempt to access the profile without logging in.

    Returns:
        None
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 401, "Expected status code 401 for unlogged profile access."
    print("Unlogged profile access failed as expected.")

def access_logged_profile(session_id: str) -> None:
    """
    Access the profile of the logged-in user.

    Args:
        session_id (str): The session ID of the logged-in user.

    Returns:
        None
    """
    response = requests.get(f"{BASE_URL}/profile", cookies={"session_id": session_id})
    assert response.status_code == 200, f"Failed to access profile: {response.text}"
    print("Logged profile accessed successfully.")

def log_out(session_id: str) -> None:
    """
    Log out the user with the given session ID.

    Args:
        session_id (str): The session ID of the user to log out.

    Returns:
        None
    """
    response = requests.delete(f"{BASE_URL}/sessions", cookies={"session_id": session_id})
    assert response.status_code == 200, f"Failed to log out: {response.text}"
    print("Logged out successfully.")

def get_reset_password_token(email_address: str) -> str:
    """
    Get the reset password token for the user with the given email address.

    Args:
        email_address (str): The email address of the user.

    Returns:
        str: The reset password token.
    """
    response = requests.post(f"{BASE_URL}/reset_password", data={"email": email_address})
    assert response.status_code == 200, f"Failed to get reset password token: {response.text}"
    reset_token = response.json()["reset_token"]
    assert reset_token is not None, "No reset password token received."
    print("Reset password token retrieved successfully.")
    return reset_token

def update_password(email_address: str, reset_token: str, new_password: str) -> None:
    """
    Update the password for the user with the given email address and reset token.

    Args:
        email_address (str): The email address of the user.
        reset_token (str): The reset password token.
        new_password (str): The new password.

    Returns:
        None
    """
    response = requests.put(f"{BASE_URL}/reset_password", data={"email": email_address, "reset_token": reset_token, "new_password": new_password})
    assert response.status_code == 200, f"Failed to update password: {response.text}"
    print("Password updated successfully.")

if __name__ == "__main__":
    user_email = "guillaume@holberton.io"
    user_password = "b4l0u"
    new_password = "t4rt1fl3tt3"

    register_user(user_email, user_password)
    log_in_wrong_password(user_email, new_password)
    access_unlogged_profile()
    session_id = log_in(user_email, user_password)
    access_logged_profile(session_id)
    log_out(session_id)
    reset_token = get_reset_password_token(user_email)
    update_password(user_email, reset_token, new_password)
    log_in(user_email, new_password)
