import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def auth_headers():
    client = TestClient(app)
    res = client.post("/api/v1/auth/register", json={
        "email": "userA@example.com",
        "password": "password123",
        "display_name": "User A"
    })
    return {"Authorization": f"Bearer {res.json()['access_token']}"}

client = TestClient(app)

def test_session_lifecycle(auth_headers):
    res = client.post("/api/v1/sessions", json={
        "language": "en",
        "goal": "reflection",
        "client_request_id": "r1"
    }, headers=auth_headers)
    assert res.status_code == 201
    session_id = res.json()["id"]
    
    res = client.post(f"/api/v1/sessions/{session_id}/messages", json={
        "client_message_id": "m1",
        "text": "Hello there."
    }, headers=auth_headers)
    assert res.status_code == 200
    assert "assistant_message" in res.json()
    
    res2 = client.post(f"/api/v1/sessions/{session_id}/messages", json={
        "client_message_id": "m1",
        "text": "Hello there."
    }, headers=auth_headers)
    assert res2.status_code == 200
    assert res2.json()["assistant_message"]["id"] == res.json()["assistant_message"]["id"]
