from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

appid = "0147c42b65d86327de81993ee6d0cd63"


def get_geolocation(city: str):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={appid}"
    response = requests.get(geo_url)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching geolocation data")

    data = response.json()
    if not data:
        raise HTTPException(status_code=404, detail="City not found")

    geolocation = {"lat": data[0]['lat'], "lon": data[0]['lon']}

    return geolocation
