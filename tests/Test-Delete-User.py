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
            "username": f"delete_test_user{unique_number}",
            "email": f"delete_test{unique_number}@example.com",
            "password": "Ab12345",
            "age": 30,
            "phone": "0987654321"
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

    def test_delete_user_success(self, client):
        token = self.login_and_get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        delete_response = client.delete(f"{BASE_URL}/users/{self.user_id}", headers=headers)
        assert delete_response.status_code == 200
        pprint.pprint(delete_response.json())


        get_response = client.get(f"{BASE_URL}/users/{self.user_id}", headers=headers)
        assert get_response.status_code == 422

    def test_delete_user_invalid_token(self, client):
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.delete(f"{BASE_URL}/users/{self.user_id}", headers=headers)
        assert response.status_code == 401
        pprint.pprint(response.json())

    def test_delete_user_empty_token(self, client):
        headers = {"Authorization": "Bearer "}
        response = client.delete(f"{BASE_URL}/users/{self.user_id}", headers=headers)
        assert response.status_code == 422
        pprint.pprint(response.json())

    def test_delete_nonexistent_user(self, client):
        token = self.login_and_get_token(client)
        headers = {"Authorization": f"Bearer {token}"}
        nonexistent_user_id = 999999
        response = client.delete(f"{BASE_URL}/users/{nonexistent_user_id}", headers=headers)

        assert response.status_code in [404, 422]
        pprint.pprint(response.json())

