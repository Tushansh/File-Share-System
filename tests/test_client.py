import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app.models import File
from app.utils import encrypt_id

client = TestClient(app)

Base.metadata.create_all(bind=engine)

def test_list_files():
    # Login as verified client
    login_data = {
        "username": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/client/files", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_generate_download_link():
    login_data = {
        "username": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    files_response = client.get("/client/files", headers=headers)
    files = files_response.json()
    if not files:
        pytest.skip("No files to download")

    file_id = files[0]["id"]
    response = client.get(f"/client/download-file/{file_id}", headers=headers)
    assert response.status_code == 200
    assert "download_link" in response.json()

def test_download_file():
    login_data = {
        "username": "testuser@example.com",
        "password": "testpassword"
    }
    response = client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    db = SessionLocal()
    file = db.query(File).first()
    if not file:
        pytest.skip("No files in database")

    enc_id = encrypt_id(file.id)
    response = client.get(f"/client/download/{enc_id}", headers=headers)
    assert response.status_code == 200
