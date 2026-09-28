from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add_and_list_reading():
    response = client.post("/readings", json={"sensor_id": "salon", "temperature": 22.5})
    assert response.status_code == 201

    response = client.get("/readings", params={"sensor_id": "salon"})
    assert len(response.json()) == 1