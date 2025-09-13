import pytest
from fastapi.testclient import TestClient
from main import app
import pprint
import random

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)

class TestUserAPI:

    @pytest.fixture(autouse=True)
    def setup_user(self, client):
        unique_number = random.randint(1, 10000)
        payload_create = {
            "username": f"logout_test_user{unique_number}",
            "email": f"melike+logout{unique_number}@example.com",
            "password": "Ab12345",
            "age": 25,
            "phone": "1234567890"
        }
        post_response = client.post(f"{BASE_URL}/users/", json=payload_create)
        assert post_response.status_code == 201
        self.user_payload = payload_create

    def login_and_get_token(self, client):
        login_payload = {
            "username": self.user_payload["username"],
            "password": self.user_payload["password"]
        }
        login_response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert login_response.status_code == 200
        login_data = login_response.json()
        token = login_data.get("access_token") or login_data.get("token") or login_data.get("auth_token")
        assert token is not None
        return token

    def test_logout_success(self, client):
        token = self.login_and_get_token(client)
        logout_payload = {"token": token}
        response = client.post(f"{BASE_URL}/logout", json=logout_payload)
        assert response.status_code in [200, 204]
        pprint.pprint(response.json())
        # ---------- NEGATIVE SCENARIOS ----------
    def test_logout_invalid_token(self, client):
        logout_payload = {"token": "invalid_token"}
        response = client.post(f"{BASE_URL}/logout", json=logout_payload)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_logout_empty_token(self, client):
        logout_payload = {"token": ""}
        response = client.post(f"{BASE_URL}/logout", json=logout_payload)
        assert response.status_code == 422
        pprint.pprint(response.json())
