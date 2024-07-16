from fastapi import HTTPException

from main import get_geolocation


def test_get_geolocation_valid_city():
    geolocation = get_geolocation("Belfast")
    assert geolocation['lat'] == 54.596391
    assert geolocation['lon'] == -5.9301829


def test_get_geolocation_invalid_city():
    try:
        get_geolocation("Notrealfast")
    except HTTPException as e:
        assert e.status_code == 404
        assert e.detail == "City not found"
