import requests
import random
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"  # Replace with your server's base URL
HEADERS = {"Content-Type": "application/json"}

# User credentials
user_credentials = {
    "username": "akhilsankerreekithak@gmail.com",
    "password": "PasswordTestKAMLeads2024"
}

# Helper Functions
def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def login_user():
    response = requests.post(f"{BASE_URL}/auth/login", json=user_credentials, headers=HEADERS)
    if response.status_code != 200:
        print(f"Login Failed: {response.json()}")
        return None
    token = response.json().get("access_token")
    HEADERS["Authorization"] = f"Bearer {token}"
    print("Login successful!")
    return token

def create_kam(name, email):
    kam_data = {"name": name, "email": email}
    response = requests.post(f"{BASE_URL}/kams/", json=kam_data, headers=HEADERS)
    if response.status_code == 201:
        return response.json()["id"]
    print(f"KAM creation failed: {response.json()}")
    return None

def create_lead(restaurant_name, call_frequency_days, status="NEW"):
    lead_data = {
        "restaurant_name": restaurant_name,
        "call_frequency_days": call_frequency_days,
        "status": status
    }
    response = requests.post(f"{BASE_URL}/leads/", json=lead_data, headers=HEADERS)
    if response.status_code == 201:
        return response.json()["id"]
    print(f"Lead creation failed: {response.json()}")
    return None

def add_contact(lead_id, name, role, contact_info):
    contact_data = {"name": name, "role": role, "contact_info": contact_info}
    response = requests.post(f"{BASE_URL}/contacts/{lead_id}/", json=contact_data, headers=HEADERS)
    if response.status_code != 201:
        print(f"Contact creation failed for lead {lead_id}: {response.json()}")

def add_interaction(lead_id, details, interaction_type="CALL", outcome="PENDING"):
    interaction_data = {
        "details": details,
        "type": interaction_type,
        "outcome": outcome,
        "interaction_date": random_date(datetime.now() - timedelta(days=30), datetime.now()).isoformat()
    }
    response = requests.post(f"{BASE_URL}/interactions/{lead_id}/", json=interaction_data, headers=HEADERS)
    if response.status_code != 201:
        print(f"Interaction creation failed for lead {lead_id}: {response.json()}")

# Bulk Data Population
def populate_data():
    # Login
    token = login_user()
    if not token:
        print("Cannot proceed without authentication.")
        return

    # Create a KAM
    # kam_id = create_kam("Akhil Manager", "kam1@gmail.com")
    # if not kam_id:
    #     print("Cannot proceed without a KAM.")
    #     return

    # Create leads and associated data
    for i in range(20, 40):  # Generate 20 leads
        lead_name = f"Restaurant {i + 1}"
        lead_id = create_lead(lead_name, random.randint(5, 15))
        if not lead_id:
            continue

        # Add 3 contacts per lead
        for j in range(3):
            add_contact(
                lead_id,
                name=f"Contact {j + 1} for {lead_name}",
                role=random.choice(["Manager", "Chef", "Owner"]),
                contact_info=f"{lead_name.lower().replace(' ', '_')}_{j + 1}@example.com"
            )

        # Add 5 interactions per lead
        for k in range(5):
            add_interaction(
                lead_id,
                details=f"Interaction {k + 1} for {lead_name}",
                interaction_type=random.choice(["CALL", "MEETING", "EMAIL"]),
                outcome=random.choice(["SUCCESSFUL", "PENDING", "FAILED"])
            )

    print("Bulk data population complete!")

# Run the script
populate_data()
