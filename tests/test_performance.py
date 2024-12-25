# tests/test_performance.py

import pytest
from datetime import datetime, timedelta
from tests.confest import *


@pytest.fixture
def lead_with_interactions(client, auth_headers):
    """
    Creates a lead, then adds some interactions.
    Returns the lead JSON.
    """
    # 1) Create a lead
    lead_payload = {"restaurant_name": "Performance Test Lead", "status": "IN_PROGRESS"}
    lead_resp = client.post("/leads/", json=lead_payload, headers=auth_headers)
    assert lead_resp.status_code == 200, lead_resp.text
    lead = lead_resp.json()

    # 2) Add a couple of interactions (both recent)
    # For the sake of the example, let's just assume each interaction_date is "now" by default
    # or you can later patch them if your logic requires a specific date.
    interactions = [
        {"details": "Recent Call #1", "type": "CALL"},
        {"details": "Recent Call #2", "type": "CALL"},
    ]
    for i in interactions:
        i_resp = client.post(
            f"/interactions/{lead['id']}", json=i, headers=auth_headers
        )
        assert i_resp.status_code == 200, i_resp.text

    return lead


def test_well_and_under_performing_leads(client, auth_headers, lead_with_interactions):
    """
    - lead_with_interactions has 2 recent interactions so far.
      We'll add a 3rd to make it 'well-performing'.
    - We'll also create another lead with 1 interaction => 'under-performing'.
    """
    # 1) Convert fixture lead to well-performing by adding 1 more interaction (total 3)
    lead_id = lead_with_interactions["id"]
    extra_interaction = {"details": "Third Call", "type": "CALL"}
    add_resp = client.post(
        f"/interactions/{lead_id}", json=extra_interaction, headers=auth_headers
    )
    assert add_resp.status_code == 200, add_resp.text

    # 2) Create a second lead with only 1 interaction => under-performing
    under_lead_payload = {"restaurant_name": "Underperforming Lead", "status": "NEW"}
    under_lead_resp = client.post(
        "/leads/", json=under_lead_payload, headers=auth_headers
    )
    assert under_lead_resp.status_code == 200, under_lead_resp.text
    under_lead = under_lead_resp.json()

    under_interaction = {"details": "Just one call", "type": "CALL"}
    ui_resp = client.post(
        f"/interactions/{under_lead['id']}",
        json=under_interaction,
        headers=auth_headers,
    )
    assert ui_resp.status_code == 200, ui_resp.text

    # 3) Check well-performing
    wp_response = client.get("/performance/well-performing", headers=auth_headers)
    assert wp_response.status_code == 200, wp_response.text
    wp_data = wp_response.json()

    wp_ids = [lead["id"] for lead in wp_data]
    assert (
        lead_with_interactions["id"] in wp_ids
    ), "The lead with 3 interactions should be in the well-performing list."

    # 4) Check under-performing
    up_response = client.get("/performance/under-performing", headers=auth_headers)
    assert up_response.status_code == 200, up_response.text
    up_data = up_response.json()

    up_ids = [lead["id"] for lead in up_data]
    assert (
        under_lead["id"] in up_ids
    ), "The lead with only 1 interaction should be in the under-performing list."
