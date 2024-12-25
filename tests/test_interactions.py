# tests/test_interactions.py

import pytest
from tests.confest import *
from datetime import datetime


@pytest.fixture
def lead_for_interactions(client, auth_headers):
    """
    Creates a fresh lead used specifically for testing interactions.
    Returns the created lead's JSON data.
    """
    payload = {"restaurant_name": "Interaction Test Restaurant", "status": "NEW"}
    response = client.post("/leads/", json=payload, headers=auth_headers)
    assert response.status_code == 200, response.text
    return response.json()


# def test_add_call_interaction_updates_last_call_date(client, lead_for_interactions, auth_headers):
#     """
#     A 'CALL' interaction should update the lead's last_call_date.
#     """
#     lead_id = lead_for_interactions["id"]
#     interaction_payload = {
#         "details": "Called the owner to discuss next order",
#         "type": "CALL"
#     }
#
#     # POST /interactions/{lead_id}
#     response = client.post(f"/interactions/{lead_id}", json=interaction_payload, headers=auth_headers)
#     assert response.status_code == 200, response.text
#
#     data = response.json()
#     assert data["id"] is not None
#     assert data["details"] == "Called the owner to discuss next order"
#     assert data["type"] == "CALL"
#     assert data["interaction_date"] is not None
#
#     # Verify that the lead's last_call_date is now updated (not None)
#     lead_check = client.get(f"/leads/{lead_id}", headers=auth_headers).json()
#     assert lead_check["last_call_date"] is not None, (
#         "Expected last_call_date to be updated after a CALL interaction"
#     )


def test_add_order_interaction_does_not_update_last_call_date(
    client, lead_for_interactions, auth_headers
):
    """
    An 'ORDER' interaction should NOT update the lead's last_call_date.
    """
    lead_id = lead_for_interactions["id"]
    # First, confirm the lead's last_call_date is None (assuming it's a fresh lead).
    # If your code or prior tests might have updated it, you may need logic
    # to verify or reset it accordingly.
    lead_initial = client.get(f"/leads/{lead_id}", headers=auth_headers).json()
    initial_last_call_date = lead_initial["last_call_date"]

    interaction_payload = {"details": "Customer placed a large order", "type": "ORDER"}

    # POST /interactions/{lead_id}
    response = client.post(
        f"/interactions/{lead_id}", json=interaction_payload, headers=auth_headers
    )
    assert response.status_code == 200, response.text

    data = response.json()
    assert data["id"] is not None
    assert data["details"] == "Customer placed a large order"
    assert data["type"] == "ORDER"
    assert data["interaction_date"] is not None

    # last_call_date should remain the same (None if fresh, or whatever it was before).
    lead_after = client.get(f"/leads/{lead_id}", headers=auth_headers).json()
    after_last_call_date = lead_after["last_call_date"]

    assert (
        after_last_call_date == initial_last_call_date
    ), "Expected last_call_date to remain unchanged after an ORDER interaction"


def test_list_interactions_for_lead(client, lead_for_interactions, auth_headers):
    """
    Verify that after adding multiple interactions, we can list them all.
    """
    lead_id = lead_for_interactions["id"]

    # Create multiple interactions
    interactions = [
        {"details": "Call #1", "type": "CALL"},
        {"details": "Order #1", "type": "ORDER"},
        {"details": "Call #2", "type": "CALL"},
    ]
    for i in interactions:
        resp = client.post(f"/interactions/{lead_id}", json=i, headers=auth_headers)
        assert resp.status_code == 200, resp.text

    # GET /interactions/{lead_id}
    response = client.get(f"/interactions/{lead_id}", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # We expect exactly 3 interactions
    assert len(data) == 3

    # Check the details match
    details_list = [item["details"] for item in data]
    assert "Call #1" in details_list
    assert "Order #1" in details_list
    assert "Call #2" in details_list


def test_add_interaction_to_non_existing_lead(client, auth_headers):
    """
    Attempting to add an interaction to a non-existent lead should return a 404.
    """
    invalid_lead_id = 999999
    interaction_payload = {"details": "Call on ghost lead", "type": "CALL"}
    response = client.post(
        f"/interactions/{invalid_lead_id}",
        json=interaction_payload,
        headers=auth_headers,
    )
    assert response.status_code == 404, response.text
    assert "Lead not found" in response.text
