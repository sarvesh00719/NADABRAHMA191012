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
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_b():
    client = TestClient(app)
    res = client.post("/api/v1/auth/register", json={
        "email": "userB@example.com",
        "password": "password123",
        "display_name": "User B"
    })
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

client = TestClient(app)

def test_create_checkin(auth_headers):
    res = client.post("/api/v1/check-ins", json={
        "mood": "good",
        "energy": "high",
        "need": "focus",
        "note": "Ready to work"
    }, headers=auth_headers)
    assert res.status_code == 201
    data = res.json()
    assert "id" in data
    assert data["mood"] == "good"

def test_invalid_checkin(auth_headers):
    res = client.post("/api/v1/check-ins", json={
        "mood": "angry",
        "energy": "high",
        "need": "focus"
    }, headers=auth_headers)
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"

def test_list_checkins(auth_headers, auth_headers_b):
    client.post("/api/v1/check-ins", json={"mood": "good", "energy": "high", "need": "focus"}, headers=auth_headers)
    client.post("/api/v1/check-ins", json={"mood": "low", "energy": "low", "need": "calm"}, headers=auth_headers)
    
    client.post("/api/v1/check-ins", json={"mood": "okay", "energy": "medium", "need": "reflect"}, headers=auth_headers_b)
    
    res_a = client.get("/api/v1/check-ins", headers=auth_headers)
    assert res_a.status_code == 200
    assert len(res_a.json()["items"]) == 2
    assert res_a.json()["trend_available"] is False
    
    res_b = client.get("/api/v1/check-ins", headers=auth_headers_b)
    assert len(res_b.json()["items"]) == 1

def test_trend_available(auth_headers):
    for _ in range(5):
        client.post("/api/v1/check-ins", json={"mood": "good", "energy": "high", "need": "focus"}, headers=auth_headers)
        
    res = client.get("/api/v1/check-ins", headers=auth_headers)
    assert len(res.json()["items"]) == 5
    assert res.json()["trend_available"] is True

def test_get_activities(auth_headers):
    res = client.get("/api/v1/activities", headers=auth_headers)
    assert res.status_code == 200
    assert "items" in res.json()

def test_post_activity_event(auth_headers):
    res = client.post("/api/v1/activities/events", json={
        "activity_key": "breathing",
        "action": "start"
    }, headers=auth_headers)
    assert res.status_code == 201

def test_post_feedback(auth_headers):
    res = client.post("/api/v1/feedback", json={
        "session_id": "S123",
        "choice": "helpful",
        "comment": "Nice session"
    }, headers=auth_headers)
    assert res.status_code == 201
