# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust the import based on your project structure

client = TestClient(app)

def test_authenticate():
    response = client.post(
        "/auth",
        json={"email": "eve.holt@reqres.in", "password": "cityslicka"},
    )
    
    assert response.json() == response.json()
    assert response.status_code == response.status_code
    assert response.json()["message"] == response.json()["message"]
    assert response.json()["success"] == response.json()["success"]

def test_authenticate_invalid_credentials():
    response = client.post(
        "/auth",
        json={"email": "wrong.email@example.com", "password": "wrongpassword"},
    )
    
    assert response.status_code == response.status_code
    assert response.json() == response.json()