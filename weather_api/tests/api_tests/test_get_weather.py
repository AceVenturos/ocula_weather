from pprint import pprint

from fastapi import HTTPException
from fastapi.testclient import TestClient
from weather_api.main import app

client = TestClient(app)


def test_get_weather_valid():
    response = client.get("/weather?city=Belfast&date=1990-07-15")
    assert response.status_code == 200
    data = response.json()
    assert "city" in data
    assert data["city"] == "Belfast"
    assert "date" in data
    assert data["date"] == "1990-07-15"
    assert "min_temp" in data
    assert data["min_temp"] == 286.73
    assert "max_temp" in data
    assert data["max_temp"] == 290.24
    assert "avg_temp" in data
    assert data["avg_temp"] == 289.40500000000003
    assert "humidity" in data
    assert data["humidity"] == 94.01


def test_get_weather_invalid_city():
    response = client.get("/weather?city=Notrealfast&date=1990-07-15")
    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}


def test_get_weather_invalid_date_past():
    response = client.get("/weather?city=Belfast&date=1979-01-01")
    assert response.status_code == 400
    # till YYYY-MM-DD will change and per OneCall API documentation it is up to 1.5 years forecast (not exact number
    # of days given
    assert 'Invalid data depth. The available data depth is from 1979-01-02 till' in response.json()['detail']

