# tests/test_contacts.py
from tests.confest import *
import pytest


@pytest.fixture
def create_lead(client, auth_headers):
    """
    Creates a Lead for testing contact addition.
    Returns the lead JSON with 'id'.
    """
    payload = {"restaurant_name": "Test Restaurant for Contacts", "status": "NEW"}
    response = client.post("/leads/", json=payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    return response.json()


def test_add_contact_to_lead(client, create_lead, auth_headers):
    """
    Verifies that we can add a single contact to a newly created lead.
    """
    lead_id = create_lead["id"]
    contact_payload = {
        "name": "John Doe",
        "role": "Manager",
        "contact_info": "john.doe@example.com",
    }
    # POST /contacts/{lead_id}
    response = client.post(
        f"/contacts/{lead_id}", json=contact_payload, headers=auth_headers
    )
    assert response.status_code == 200, response.text

    data = response.json()
    # Basic checks
    assert data["id"] is not None
    assert data["name"] == "John Doe"
    assert data["role"] == "Manager"
    assert data["contact_info"] == "john.doe@example.com"


def test_list_contacts_for_lead(client, create_lead, auth_headers):
    """
    Verifies that listing contacts for a lead returns the correct data.
    """
    lead_id = create_lead["id"]

    # Add multiple contacts
    contacts = [
        {"name": "Contact One", "role": "Owner", "contact_info": "owner@example.com"},
        {"name": "Contact Two", "role": "Chef", "contact_info": "chef@example.com"},
    ]
    for contact_data in contacts:
        resp = client.post(
            f"/contacts/{lead_id}", json=contact_data, headers=auth_headers
        )
        assert resp.status_code == 200, resp.text

    # GET /contacts/{lead_id}
    response = client.get(f"/contacts/{lead_id}", headers=auth_headers)
    assert response.status_code == 200, response.text

    data = response.json()
    # We expect exactly 2 contacts
    assert len(data) == 2

    # Check the data returned
    names = [c["name"] for c in data]
    assert "Contact One" in names
    assert "Contact Two" in names


def test_add_contact_to_non_existing_lead(client, auth_headers):
    """
    Attempting to add a contact to a non-existent lead should 404.
    """
    non_existing_lead_id = 999999999
    contact_payload = {
        "name": "Ghost Contact",
        "role": "Ghost Role",
        "contact_info": "ghost@example.com",
    }
    response = client.post(
        f"/contacts/{non_existing_lead_id}", json=contact_payload, headers=auth_headers
    )
    assert response.status_code == 404, response.text
    assert "Lead not found" in response.text
