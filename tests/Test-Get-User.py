import pytest
from fastapi.testclient import TestClient
from main import app
import pprint

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)

class TestUserAPI:

    def test_get_user_success(self, client):
        # GET all users
        response = client.get(f"{BASE_URL}/users")
        assert response.status_code == 200

        data = response.json()
        pprint.pprint(data)

        assert isinstance(data, list)
        if data:
            user = data[0]
            assert "id" in user
            assert "username" in user
            assert "email" in user

    def test_create_and_get_user_by_id(self, client):

        payload = {
            "username": "melike_test",
            "email": "meliketest+dynamic@example.com",
            "password": "Ab12345",
            "age": 25,
            "phone": "1234567890"
        }

        post_response = client.post(f"{BASE_URL}/users/", json=payload)
        assert post_response.status_code == 201
        created_user = post_response.json()
        pprint.pprint(created_user)


        get_response = client.get(f"{BASE_URL}/users")
        assert get_response.status_code == 200
        users = get_response.json()
        pprint.pprint(users)


        user_id = None
        for user in users:
            if user["email"] == payload["email"]:
                user_id = user["id"]
                break

        assert user_id is not None
        print(f"Created user ID: {user_id}")


        get_by_id_response = client.get(f"{BASE_URL}/users/{user_id}")
        assert get_by_id_response.status_code == 200
        user_by_id = get_by_id_response.json()
        pprint.pprint(user_by_id)


        assert user_by_id["id"] == user_id
        assert user_by_id["username"] == payload["username"]
        assert user_by_id["email"] == payload["email"]



