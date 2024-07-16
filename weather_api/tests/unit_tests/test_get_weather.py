from unittest.mock import patch
from fastapi.testclient import TestClient
import pytest

from weather_api.main import app

client = TestClient(app)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_get(*args, **kwargs):
    if "geo" in args[0]:
        if "Belfast" in args[0]:
            return MockResponse([{"lat": 54.596391, "lon": -5.9301829}], 200)
        elif "Notrealfast" in args[0]:
            return MockResponse([], 200)
        elif "API_Error" in args[0]:
            return MockResponse([], 500)
    elif "onecall/day_summary" in args[0]:
        if "lat=54.596391" in args[0] and "lon=-5.9301829" in args[0]:
            return MockResponse({
                "temperature": {
                    "min": 5.0,
                    "max": 15.0,
                    "morning": 10.0,
                    "afternoon": 14.0,
                    "evening": 12.0,
                    "night": 8.0
                },
                "humidity": {
                    "afternoon": 19.0
                }
            }, 200)
    return MockResponse(None, 404)


@patch('requests.get', side_effect=mock_get)
def test_get_weather_valid(mock_get):
    response = client.get("/weather?city=Belfast&date=1998-06-15")
    assert response.status_code == 200
    assert response.json() == {
        "city": "Belfast",
        "date": "1998-06-15",
        "min_temp": 5.0,
        "max_temp": 15.0,
        "avg_temp": 11.0,
        "humidity": 19.0
    }


@patch('requests.get', side_effect=mock_get)
def test_get_weather_invalid_city(mock_get):
    response = client.get("/weather?city=Notrealfast&date=2023-07-15")
    assert response.status_code == 404
    assert response.json() == {"detail": "City not found"}


@patch('requests.get', side_effect=mock_get)
def test_get_weather_api_error(mock_get):
    response = client.get("/weather?city=API_Error&date=2023-07-15")
    assert response.status_code == 500
    assert response.json() == {"detail": "Error fetching geolocation data"}

