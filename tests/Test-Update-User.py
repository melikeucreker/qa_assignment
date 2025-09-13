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
            "username": f"put_test_user{unique_number}",
            "email": f"put_test{unique_number}@example.com",
            "password": "Ab12345",
            "age": 25,
            "phone": "1234567890"
        }
        post_response = client.post(f"{BASE_URL}/users/", json=payload_create)
        assert post_response.status_code == 201
        self.user_payload = payload_create
        self.user_id = post_response.json()["id"]

    def login_and_get_token(self, client):
        login_payload = {
            "username": self.user_payload["username"],
            "password": self.user_payload["password"]
        }
        login_response = client.post(f"{BASE_URL}/login", json=login_payload)
        assert login_response.status_code == 200
        token = login_response.json().get("access_token") or login_response.json().get("token") or login_response.json().get("auth_token")
        assert token is not None
        return token

    def test_update_user_success(self, client):
        token = self.login_and_get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        payload_update = {
            "email": "user@example.com",
            "age": 18,
            "phone": "string"
        }
        put_response = client.put(f"{BASE_URL}/users/{self.user_id}", json=payload_update, headers=headers)
        assert put_response.status_code == 200
        updated_user = put_response.json()
        pprint.pprint(updated_user)

    def test_update_user_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid_token"}
        payload_update = {
            "email": "user@example.com",
            "age": 18,
            "phone": "string"
        }
        response = client.put(f"{BASE_URL}/users/{self.user_id}", json=payload_update, headers=headers)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_update_user_empty_token(self, client):
        headers = {"Authorization": "Bearer "}
        payload_update = {
            "email": "user@example.com",
            "age": 18,
            "phone": "string"
        }
        response = client.put(f"{BASE_URL}/users/{self.user_id}", json=payload_update, headers=headers)
        assert response.status_code == 401
        pprint.pprint(response.json())
