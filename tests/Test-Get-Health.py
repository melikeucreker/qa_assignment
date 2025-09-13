import pytest
from fastapi.testclient import TestClient
from main import app
import pprint

BASE_URL = "http://localhost:8000"

@pytest.fixture
def client():
    return TestClient(app)

class TestHealthAPI:

    def test_health_status(self, client):
        response = client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        data = response.json()
        pprint.pprint(data)
        assert "status" in data
        assert data["status"] in ["healthy", "ok"]
        if "uptime" in data:
            assert isinstance(data["uptime"], (int, float))
        if "version" in data:
            assert isinstance(data["version"], str)
