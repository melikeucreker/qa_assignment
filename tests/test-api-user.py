import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestUserAPI:
    def test_user_creation(self, client):
        payload = {
            "username": "melike",
            "email": "meliketest+test1@example.com",
            "password": "aB123456",
            "age": 18,
            "phone": "4555673723"
        }

        response = client.post("/users/", json=payload)


        print(response.status_code)
        print(response.json())

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert data["age"] == payload["age"]
        assert data["phone"] == payload["phone"]
