import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Shared variables for tests
test_user = {"username": "testuser@example.com", "password": "password123"}
auth_token = None
lead_id = None
kam_id = None


@pytest.fixture(scope="module")
def login_token():
    """Fixture to login and retrieve an auth token."""
    # Register user if not already registered
    response = client.post("/auth/register", json=test_user)
    if response.status_code not in [200, 201]:
        assert response.status_code == 400  # Expected if user already exists
        assert response.json()["detail"] == "Username already registered"

    # Login the user
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200, f"Login failed: {response.json()}"
    return response.json()["access_token"]


def test_register_user():
    """Test user registration."""
    response = client.post("/auth/register", json=test_user)
    if response.status_code == 400:  # User already exists
        assert response.json()["detail"] == "Username already registered"
    else:
        assert response.status_code in [200, 201], f"Register failed: {response.json()}"


def test_login_user(login_token):
    """Test user login."""
    assert login_token is not None


def test_create_kam(login_token):
    """Test creating a KAM."""
    global kam_id
    headers = {"Authorization": f"Bearer {login_token}"}
    kam_data = {"name": "John Manager", "email": "johnmanager@example.com"}
    response = client.post("/kams/", json=kam_data, headers=headers)
    if response.status_code == 400:  # KAM already exists
        assert "already exists" in response.json()["detail"]
    else:
        assert response.status_code == 201, f"KAM creation failed: {response.json()}"
        kam_id = response.json()["id"]


def test_get_kams(login_token):
    """Test retrieving all KAMs."""
    headers = {"Authorization": f"Bearer {login_token}"}
    response = client.get("/kams/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_lead(login_token):
    """Test creating a lead."""
    global lead_id
    headers = {"Authorization": f"Bearer {login_token}"}
    lead_data = {"restaurant_name": "Test Restaurant", "call_frequency_days": 7}
    response = client.post("/leads/", json=lead_data, headers=headers)
    if response.status_code == 400:  # Lead already exists
        assert "already exists" in response.json()["detail"]
    else:
        assert response.status_code == 201, f"Lead creation failed: {response.json()}"
        lead_id = response.json()["id"]


def test_get_leads(login_token):
    """Test retrieving all leads."""
    headers = {"Authorization": f"Bearer {login_token}"}
    response = client.get("/leads/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_contact(login_token):
    """Test adding a contact to a lead."""
    headers = {"Authorization": f"Bearer {login_token}"}
    contact_data = {
        "name": "Jane Doe",
        "role": "Manager",
        "contact_info": "janedoe@example.com",
    }
    response = client.post(f"/contacts/{lead_id}/", json=contact_data, headers=headers)
    assert response.status_code == 201, f"Contact addition failed: {response.json()}"


def test_get_contacts(login_token):
    """Test retrieving contacts for a lead."""
    headers = {"Authorization": f"Bearer {login_token}"}
    response = client.get(f"/contacts/{lead_id}/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_interaction(login_token):
    """Test adding an interaction to a lead."""
    headers = {"Authorization": f"Bearer {login_token}"}
    interaction_data = {"details": "Test call", "type": "CALL", "outcome": "PENDING"}
    response = client.post(
        f"/interactions/{lead_id}/", json=interaction_data, headers=headers
    )
    assert (
        response.status_code == 201
    ), f"Interaction addition failed: {response.json()}"


def test_get_interactions(login_token):
    """Test retrieving interactions for a lead."""
    headers = {"Authorization": f"Bearer {login_token}"}
    response = client.get(f"/interactions/{lead_id}/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
