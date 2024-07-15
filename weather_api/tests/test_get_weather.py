from fastapi.testclient import TestClient
from weather_api.main import app

client = TestClient(app)


def test_get_weather():
    response = client.get("/weather?city=Belfast&date=1990-07-15")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert data["city"] == "Belfast"
    assert "date" in data
    assert data["date"] == "1990-07-15"
    assert "min_temp" in data
    assert data["min_temp"] == "286.73"
    assert "max_temp" in data
    assert data["max_temp"] == "290.24"
    assert "avg_temp" in data
    assert data["avg_temp"] == "289.40500000000003"
    assert "humidity" in data
    assert data["humidity"] == "94.01"
