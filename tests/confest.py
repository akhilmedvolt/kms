import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app import models


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def get_token(client):
    register_payload = {"username": "globaltestuser", "password": "globaltestpass"}
    client.post("/auth/register", json=register_payload)

    login_response = client.post("/auth/login", json=register_payload)
    assert login_response.status_code == 200, login_response.text
    data = login_response.json()
    return data["access_token"]


@pytest.fixture
def auth_headers(get_token):
    return {"Authorization": f"Bearer {get_token}"}
