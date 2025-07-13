import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from sqlalchemy.orm import Session
from app import models

client = TestClient(app)

# Initialize DB schema for testing
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def test_user():
    return {
        "email": "testuser@example.com",
        "password": "testpassword",
        "user_type": "client"
    }

def test_signup(test_user):
    response = client.post("/auth/signup", json=test_user)
    assert response.status_code == 200
    assert "verify_url" in response.json()

def test_login_unverified(test_user):
    data = {"username": test_user["email"], "password": test_user["password"]}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 403  # not verified yet

def test_verify_email(test_user):
    db: Session = SessionLocal()
    user = db.query(models.User).filter(models.User.email == test_user["email"]).first()
    token = user.id
    from app.utils import encrypt_id
    enc_id = encrypt_id(token)
    response = client.get(f"/auth/verify/{enc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"

def test_login_verified(test_user):
    data = {"username": test_user["email"], "password": test_user["password"]}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    assert "access_token" in response.json()
