import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import User

client = TestClient(app)

Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="module")
def ops_user():
    return {
        "email": "opsuser@example.com",
        "password": "opspassword",
        "user_type": "ops"
    }

def test_signup_ops(ops_user):
    response = client.post("/auth/signup", json=ops_user)
    assert response.status_code == 200

def test_verify_ops_email(ops_user):
    db = SessionLocal()
    user = db.query(User).filter(User.email == ops_user["email"]).first()
    from app.utils import encrypt_id
    enc_id = encrypt_id(user.id)
    response = client.get(f"/auth/verify/{enc_id}")
    assert response.status_code == 200

def test_login_ops(ops_user):
    data = {"username": ops_user["email"], "password": ops_user["password"]}
    response = client.post("/auth/login", data=data)
    assert response.status_code == 200
    global ops_token
    ops_token = response.json()["access_token"]

def test_upload_valid_file():
    headers = {"Authorization": f"Bearer {ops_token}"}
    with open("sample.docx", "wb") as f:
        f.write(b"Fake Word Content")

    with open("sample.docx", "rb") as f:
        response = client.post("/ops/upload", files={"upload": ("sample.docx", f)}, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "File uploaded successfully"

def test_upload_invalid_file():
    headers = {"Authorization": f"Bearer {ops_token}"}
    with open("bad_file.txt", "wb") as f:
        f.write(b"Text file not allowed")

    with open("bad_file.txt", "rb") as f:
        response = client.post("/ops/upload", files={"upload": ("bad_file.txt", f)}, headers=headers)
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"