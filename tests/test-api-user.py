import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)
class TestUserAPI:
    def test_user_creation(self,client):
        payload = {

                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "aB12",
                "age": 18,
                "phone": "4555673723"

        }

       #Positive Case
        response = client.post("/users/", json=payload)

        # Asserts
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == payload["username"]
        assert data["email"] == payload["email"]
        assert data["password"] == payload["password"]
        assert data["age"] == payload["age"]
        assert data["phone"] == payload["phone"]
