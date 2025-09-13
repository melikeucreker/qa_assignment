import pytest
from fastapi.testclient import TestClient
from main import app
BASE_URL = "http://localhost:8000"
@pytest.fixture
def client():
    return TestClient(app)

class TestUserAPI:





    BASE_URL = "http://localhost:8000"



    class TestUserAPI:

        # ---------- POSITIVE SCENARIO ----------
        def test_create_user_success(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "Ab12345",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 201
            data = response.json()
            assert data["username"] == payload["username"]
            assert data["email"] == payload["email"]

        # ---------- NEGATIVE SCENARIOS ----------
        def test_create_user_missing_username(self, client):
            payload = {
                "email": "meliketest+test1@example.com",
                "password": "Ab1245",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_blank_username(self, client):
            payload = {
                "username": "",
                "email": "meliketest+test1@example.com",
                "password": "Test78798",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code in (400, 422)

        def test_create_user_missing_email(self, client):
            payload = {
                "username": "melike",
                "password": "Ab24773",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_invalid_email(self, client):
            payload = {
                "username": "melike",
                "email": "not-an-email",
                "password": "Ab12345",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_missing_password(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_short_password(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "123",
                "age": 25,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code in (400, 422)

        def test_create_user_missing_age(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "ValidPass123",
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_negative_age(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "ValidPass123",
                "age": -5,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_missing_phone(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "ValidPass123",
                "age": 25
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_invalid_phone(self, client):
            payload = {
                "username": "melike",
                "email": "meliketest+test1@example.com",
                "password": "Ab1356",
                "age": 25,
                "phone": "abcde123"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_empty_payload(self, client):
            response = client.post(f"{BASE_URL}/users/", json={})
            assert response.status_code == 422

        def test_create_user_no_payload(self, client):
            response = client.post(f"{BASE_URL}/users/")
            assert response.status_code == 422

        def test_create_user_min_age(self, client):
            payload = {
                "username": "min_age",
                "email": "meliketest+test1@example.com",
                "password": "minage123",
                "age": 17,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_max_age(self, client):
            payload = {
                "username": "max_age",
                "email": "meliketest+test1@example.com",
                "password": "maxage123",
                "age": 150,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422

        def test_create_user_long_username(self, client):
            payload = {
                "username": "very_long_username_that_is_close_to_fifty_chars",
                "email": "meliketest+test1@example.com",
                "password": "longpass123",
                "age": 30,
                "phone": "1234567890"
            }
            response = client.post(f"{BASE_URL}/users/", json=payload)
            assert response.status_code == 422