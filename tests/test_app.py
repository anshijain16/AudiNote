from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_returns_message():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, world"}


def test_health_returns_ok():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}