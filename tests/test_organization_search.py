from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_search_by_name(db_session) -> None:
    response = client.get(
        "/api/v1/organizations",
        params={"name": "Рога"},
        headers={"X-API-Key": "super-secret-key"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == 'ООО "Рога и Копыта"'


def test_search_by_activity_with_children(db_session) -> None:
    response = client.get(
        "/api/v1/organizations",
        params={"activity_id": 1, "include_children": True},
        headers={"X-API-Key": "super-secret-key"},
    )
    assert response.status_code == 200
    names = {item["name"] for item in response.json()}
    assert 'ООО "Рога и Копыта"' in names