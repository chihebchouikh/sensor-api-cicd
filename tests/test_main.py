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

def test_sensor_stats():
    client.post("/readings", json={"sensor_id": "cuisine", "temperature": 20.0})
    client.post("/readings", json={"sensor_id": "cuisine", "temperature": 24.0})

    response = client.get("/readings/cuisine/stats")
    assert response.status_code == 200

    data = response.json()
    assert data["count"] == 2
    assert data["average"] == 22.0
    assert data["min"] == 20.0
    assert data["max"] == 24.0


def test_sensor_stats_unknown_sensor():
    response = client.get("/readings/garage/stats")
    assert response.status_code == 404