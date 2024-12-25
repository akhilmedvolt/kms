# tests/test_call_planning.py

import pytest
from datetime import datetime, timedelta
from tests.confest import *


def test_leads_to_call_today(client, auth_headers):
    """
    Create multiple leads and verify /call-planning/today behavior:
      1) No last_call_date => should appear in the list (never called).
      2) last_call_date + frequency in the past => should appear (call overdue).
      3) last_call_date + frequency in the future => should NOT appear (call not due yet).
    """

    # 1) Lead with no last_call_date
    lead_no_call_payload = {
        "restaurant_name": "LeadNoCallDate",
        "status": "NEW",
        "call_frequency_days": 7,
    }
    lead_no_call = client.post(
        "/leads/", json=lead_no_call_payload, headers=auth_headers
    ).json()

    # 2) Lead with last_call_date that is past due
    #    We'll create the lead normally, then update last_call_date to 10 days ago
    lead_past_due_payload = {
        "restaurant_name": "LeadPastDue",
        "status": "NEW",
        "call_frequency_days": 7,
    }
    lead_past_due = client.post(
        "/leads/", json=lead_past_due_payload, headers=auth_headers
    ).json()
    old_date = (datetime.utcnow() - timedelta(days=10)).isoformat()
    lead_past_due["last_call_date"] = old_date
    # Update the lead via PUT
    client.put(
        f"/leads/{lead_past_due['id']}", json=lead_past_due, headers=auth_headers
    )

    # 3) Lead with last_call_date that is NOT yet due
    #    For example, last call was 3 days ago but frequency is 10 days
    lead_not_due_payload = {
        "restaurant_name": "LeadNotDue",
        "status": "NEW",
        "call_frequency_days": 10,
    }
    lead_not_due = client.post(
        "/leads/", json=lead_not_due_payload, headers=auth_headers
    ).json()
    future_date = (datetime.utcnow() - timedelta(days=3)).isoformat()
    lead_not_due["last_call_date"] = future_date
    # Update the lead via PUT
    client.put(f"/leads/{lead_not_due['id']}", json=lead_not_due, headers=auth_headers)

    # Now call /call-planning/today
    response = client.get("/call-planning/today", headers=auth_headers)
    assert response.status_code == 200, response.text
    data = response.json()

    # Convert the returned leads to a set of IDs for easy membership checks
    returned_lead_ids = {lead["id"] for lead in data}

    # 1) Should be in today's call list (never called)
    assert lead_no_call["id"] in returned_lead_ids

    # 2) Should be in today's call list (call is overdue)
    assert lead_past_due["id"] in returned_lead_ids

    # 3) Should NOT be in today's list (not due yet)
    assert lead_not_due["id"] not in returned_lead_ids
