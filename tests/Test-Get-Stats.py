import pytest
from fastapi.testclient import TestClient
from main import app
import pprint

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)

class TestStatsAPI:

    def test_stats_default(self, client):
        response = client.get(f"{BASE_URL}/stats")
        assert response.status_code == 200
        data = response.json()
        pprint.pprint(data)
        assert "session_tokens" not in data or data.get("session_tokens") == []
        assert "user_emails" not in data or data.get("user_emails") == []

    def test_stats_include_details_true(self, client):
        params = {"include_details": "true"}
        response = client.get(f"{BASE_URL}/stats", params=params)
        assert response.status_code == 200
        data = response.json()
        pprint.pprint(data)
        assert "session_tokens" in data
        assert "user_emails" in data

    def test_stats_include_details_false(self, client):
        params = {"include_details": "false"}
        response = client.get(f"{BASE_URL}/stats", params=params)
        assert response.status_code == 200
        data = response.json()
        pprint.pprint(data)
        assert "session_tokens" not in data or data.get("session_tokens") == []
        assert "user_emails" not in data or data.get("user_emails") == []

