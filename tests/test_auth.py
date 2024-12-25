# tests/test_auth.py

import pytest
from tests.confest import *


def test_register_user(client):
    """
    Tests user registration for a new username.
    """
    payload = {"username": "auth_test_user", "password": "auth_test_pass"}

    # Attempt registration
    response = client.post("/auth/register", json=payload)

    # If user was never registered, should be 200
    # If user was already registered, could be 400 ("Username already registered")
    assert response.status_code in (200, 400)

    # If it's 200, the user was newly created
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert "username" in data
        assert data["username"] == "auth_test_user"


def test_login_user(client):
    """
    Tests user login, ensuring we get a valid JWT token.
    """
    reg_payload = {"username": "login_tester", "password": "tester_pass"}
    # Register (ignore if 400 means user already exists)
    client.post("/auth/register", json=reg_payload)

    # Now login
    response = client.post("/auth/login", json=reg_payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    # You could decode or further assert token structure if needed


def test_me_endpoint(auth_headers, client):
    """
    Tests the /auth/me endpoint using the auth_headers fixture.
    """
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    # In conftest.py, we registered/logged in with "globaltestuser"
    # So we expect that username here
    assert data["username"] == "globaltestuser"
    assert data["is_active"] is True
