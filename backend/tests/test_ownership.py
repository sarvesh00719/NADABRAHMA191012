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

def test_cross_user_access_fails():
    res_a = client.post("/api/v1/auth/register", json={"email": "a@example.com", "password": "password123", "display_name": "A"})
    token_a = res_a.json()["access_token"]
    
    res_b = client.post("/api/v1/auth/register", json={"email": "b@example.com", "password": "password123", "display_name": "B"})
    token_b = res_b.json()["access_token"]
    
    s_res = client.post("/api/v1/sessions", json={"language": "en", "goal": "reflection"}, headers={"Authorization": f"Bearer {token_a}"})
    session_id = s_res.json()["id"]
    
    m_res = client.post(f"/api/v1/sessions/{session_id}/messages", json={"text": "hello"}, headers={"Authorization": f"Bearer {token_b}"})
    assert m_res.status_code == 404
