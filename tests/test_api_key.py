from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_key_required() -> None:
    response = client.get("/api/v1/buildings")
    assert response.status_code == 422


def test_invalid_api_key() -> None:
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401


def test_valid_api_key(db_session) -> None:
    response = client.get("/api/v1/buildings", headers={"X-API-Key": "super-secret-key"})
    assert response.status_code == 200
    assert len(response.json()) >= 1