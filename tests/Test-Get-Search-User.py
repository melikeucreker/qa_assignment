import pytest
from fastapi.testclient import TestClient
from main import app
import random
import pprint

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)

class TestUserSearchAPI:

    @pytest.fixture(autouse=True)
    def setup_users(self, client):

        self.users = []
        for i in range(3):
            unique_number = random.randint(1, 10000)
            payload = {
                "username": f"search_user{unique_number}",
                "email": f"melike+search{unique_number}@example.com",
                "password": "Ab12345",
                "age": 25,
                "phone": "1234567890"
            }
            post_response = client.post(f"{BASE_URL}/users/", json=payload)
            assert post_response.status_code == 201
            self.users.append(payload)

    def test_search_by_username_partial(self, client):
        partial_username = self.users[0]["username"][:6]
        params = {"q": partial_username, "field": "username", "exact": "false"}
        response = client.get(f"{BASE_URL}/users/search", params=params)
        assert response.status_code == 200
        results = response.json()
        pprint.pprint(results)
        assert any(user["username"] == self.users[0]["username"] for user in results)

    def test_search_by_email_exact(self, client):
        email = self.users[1]["email"]
        params = {"q": email, "field": "email", "exact": "true"}
        response = client.get(f"{BASE_URL}/users/search", params=params)
        assert response.status_code == 200
        results = response.json()
        pprint.pprint(results)
        assert len(results) == 1
        assert results[0]["email"] == email

    def test_search_all_fields_partial(self, client):
        keyword = self.users[2]["username"][:5]
        params = {"q": keyword, "field": "all", "exact": "false"}
        response = client.get(f"{BASE_URL}/users/search", params=params)
        assert response.status_code == 200
        results = response.json()
        pprint.pprint(results)
        assert any(user["username"] == self.users[2]["username"] for user in results)

    def test_search_no_results(self, client):
        params = {"q": "nonexistentuser12345", "field": "all", "exact": "false"}
        response = client.get(f"{BASE_URL}/users/search", params=params)
        assert response.status_code == 200
        results = response.json()
        pprint.pprint(results)
        assert results == []
