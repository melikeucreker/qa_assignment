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
            "username": f"login_test_user{unique_number}",
            "email": f"melike+test{unique_number}@example.com",
            "password": "Ab12345",
            "age": 25,
            "phone": "1234567890"
        }
        post_response = client.post(f"{BASE_URL}/users/", json=payload_create)
        assert post_response.status_code == 201
        self.user_payload = payload_create

    def test_login_success(self, client):
        login_payload = {
            "username": self.user_payload["username"],
            "password": self.user_payload["password"]
        }
        response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert response.status_code == 200
        login_data = response.json()
        pprint.pprint(login_data)
        token = login_data.get("access_token") or login_data.get("token") or login_data.get("auth_token")
        assert token is not None

    def test_login_invalid_username(self, client):
        login_payload = {
            "username": "wrong_username",
            "password": self.user_payload["password"]
        }
        response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_login_invalid_password(self, client):
        login_payload = {
            "username": self.user_payload["username"],
            "password": "wrong_password"
        }
        response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_login_invalid_both(self, client):
        login_payload = {
            "username": "wrong_username",
            "password": "wrong_password"
        }
        response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_login_empty_payload(self, client):
        login_payload = {
            "username": "",
            "password": ""
        }
        response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert response.status_code == 401
        pprint.pprint(response.json())

