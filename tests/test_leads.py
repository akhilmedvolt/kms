# tests/test_leads.py

import pytest
from tests.confest import *


@pytest.fixture
def cleanup_lead_ids():
    """
    Optional fixture to keep track of created leads.
    Could be used to clean up (delete) them after tests if desired.
    """
    lead_ids = []
    yield lead_ids
    # If you want to delete them after the test, uncomment:
    # for lid in lead_ids:
    #     # You need the client fixture here if you actually want to delete
    #     client.delete(f"/leads/{lid}", headers=auth_headers)


def test_create_lead(client, auth_headers, cleanup_lead_ids):
    """
    Tests the creation of a new lead.
    """
    payload = {"restaurant_name": "Test Restaurant", "status": "NEW"}
    response = client.post("/leads/", json=payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Basic checks
    assert "id" in data
    assert data["restaurant_name"] == "Test Restaurant"
    assert data["status"] == "NEW"

    # Keep track of lead IDs if needed
    cleanup_lead_ids.append(data["id"])


def test_list_leads(client, auth_headers):
    """
    Ensures we can list leads without error and the response is a list.
    """
    response = client.get("/leads/", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)


def test_get_lead_by_id(client, auth_headers):
    """
    Create a lead, then retrieve it by ID to verify correctness.
    """
    # 1) Create lead
    create_payload = {"restaurant_name": "Specific Lead", "status": "IN_PROGRESS"}
    create_resp = client.post("/leads/", json=create_payload, headers=auth_headers)
    assert create_resp.status_code == 200, create_resp.text
    created_lead = create_resp.json()

    # 2) Get the newly created lead by ID
    get_resp = client.get(f"/leads/{created_lead['id']}", headers=auth_headers)
    assert get_resp.status_code == 200, get_resp.text
    fetched_lead = get_resp.json()

    assert fetched_lead["id"] == created_lead["id"]
    assert fetched_lead["restaurant_name"] == "Specific Lead"
    assert fetched_lead["status"] == "IN_PROGRESS"


def test_update_lead(client, auth_headers):
    """
    Create a lead, then update some fields.
    """
    # 1) Create lead
    create_payload = {"restaurant_name": "LeadToUpdate", "status": "NEW"}
    create_resp = client.post("/leads/", json=create_payload, headers=auth_headers)
    assert create_resp.status_code == 200, create_resp.text
    lead = create_resp.json()

    # 2) Update it
    update_payload = {
        "restaurant_name": "LeadRenamed",
        "status": "WON",
        "call_frequency_days": 14,
    }
    update_resp = client.put(
        f"/leads/{lead['id']}", json=update_payload, headers=auth_headers
    )
    assert update_resp.status_code == 200, update_resp.text
    updated_lead = update_resp.json()

    assert updated_lead["restaurant_name"] == "LeadRenamed"
    assert updated_lead["status"] == "WON"
    assert updated_lead["call_frequency_days"] == 14


def test_delete_lead(client, auth_headers):
    """
    Create a lead, then delete it, verifying it is indeed removed.
    """
    # 1) Create lead
    create_payload = {"restaurant_name": "LeadToDelete", "status": "NEW"}
    create_resp = client.post("/leads/", json=create_payload, headers=auth_headers)
    assert create_resp.status_code == 200, create_resp.text
    lead = create_resp.json()

    # 2) Delete lead
    del_resp = client.delete(f"/leads/{lead['id']}", headers=auth_headers)
    assert del_resp.status_code == 200, del_resp.text
    # Optionally, check the message or JSON if your route returns more detail:
    # assert del_resp.json().get("msg") == "Lead deleted successfully"

    # 3) Attempt to GET the deleted lead
    get_resp = client.get(f"/leads/{lead['id']}", headers=auth_headers)
    assert get_resp.status_code == 200, get_resp.text

    # Depending on how your code handles "not found" leads, you might get None or a 404.
    # If your code always returns 200 (with lead=None), do:
    fetched_lead = get_resp.json()
    assert (
        fetched_lead is None or fetched_lead == {}
    ), "Expected no data for a deleted lead"
