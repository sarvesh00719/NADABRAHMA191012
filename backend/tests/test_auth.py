import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register():
    res = client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "password123",
        "display_name": "Test User"
    })
    assert res.status_code == 201
    data = res.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_register_duplicate_email():
    client.post("/api/v1/auth/register", json={
        "email": "test2@example.com",
        "password": "password123",
        "display_name": "User 1"
    })
    res = client.post("/api/v1/auth/register", json={
        "email": "test2@example.com",
        "password": "password123",
        "display_name": "User 2"
    })
    assert res.status_code == 409
    assert res.json()["error"]["code"] == "EMAIL_TAKEN"

def test_login():
    client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "password123",
        "display_name": "Login User"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "password123"
    })
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_wrong_password():
    client.post("/api/v1/auth/register", json={
        "email": "wrong@example.com",
        "password": "password123",
        "display_name": "Wrong User"
    })
    res = client.post("/api/v1/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpassword"
    })
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "INVALID_CREDENTIALS"

def test_me_with_token():
    reg_res = client.post("/api/v1/auth/register", json={
        "email": "me@example.com",
        "password": "password123",
        "display_name": "Me User"
    })
    token = reg_res.json()["access_token"]
    
    res = client.get("/api/v1/me", headers={"Authorization": f"Bearer {token}"})
    assert res.status_code == 200
    assert res.json()["email"] == "me@example.com"
    assert res.json()["preferences"]["language"] == "en"

def test_me_without_token():
    res = client.get("/api/v1/me")
    assert res.status_code in (401, 403)

def test_me_expired_token():
    res = client.get("/api/v1/me", headers={"Authorization": "Bearer bad_token"})
    assert res.status_code == 401
    assert res.json()["error"]["code"] == "UNAUTHORIZED"

