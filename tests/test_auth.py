from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_auth_normal_flow():
    payload = {"email": "eve.holt@reqres.in","password": "cityslicka"}
    response = client.post("/auth",json=payload)

    json_response = response.json()

    # assert the json response status & message output
    assert json_response["status_code"] == 200
    assert json_response["message"] == "Login successful"
    assert json_response["success"] is True

    # assert data field
    assert "data" in json_response
    assert isinstance(json_response["data"], dict)
    assert "email" in json_response["data"]
    assert "password" in json_response["password"]
    assert "token" in json_response["data"]
