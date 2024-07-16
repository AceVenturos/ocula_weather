from unittest.mock import patch
from fastapi import HTTPException
import requests

from main import get_geolocation


def mock_get(*args, **kwargs):
    if args[0].startswith("http://api.openweathermap.org/geo/1.0/direct?q=Belfast"):
        return MockResponse([{"lat": 54.596391, "lon": -5.9301829}], 200)
    elif args[0].startswith("http://api.openweathermap.org/geo/1.0/direct?q=Notrealfast"):
        return MockResponse([], 200)
    elif args[0].startswith("http://api.openweathermap.org/geo/1.0/direct?q=ApiError"):
        return MockResponse(None, 500)
    return MockResponse(None, 404)


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


@patch('requests.get', side_effect=mock_get)
def test_get_geolocation_valid_city(mock_get):
    geolocation = get_geolocation("Belfast")
    assert geolocation['lat'] == 54.596391
    assert geolocation['lon'] == -5.9301829


@patch('requests.get', side_effect=mock_get)
def test_get_geolocation_invalid_city(mock_get):
    try:
        get_geolocation("Notrealfast")
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "City not found"


@patch('requests.get', side_effect=mock_get)
def test_get_geolocation_api_error(mock_get):
    try:
        get_geolocation("ApiError")
    except HTTPException as e:
        assert e.status_code == 500
        assert e.detail == "Error fetching geolocation data"
