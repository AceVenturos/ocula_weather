from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

from pprint import pprint

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


class WeatherResponse(BaseModel):
    city: str
    min_temp: float
    max_temp: float
    avg_temp: float
    humidity: float


@app.get("/weather", response_model=WeatherResponse)
def get_weather(city: str, date: str):
    geolocation = get_geolocation(city)

    url = (f"https://api.openweathermap.org/data/3.0/onecall/day_summary?"
           f"lat={geolocation['lat']}&lon={geolocation['lon']}&date={date}&appid={appid}")
    response = requests.get(url)
    data = response.json()

    pprint(data)

    min_temp = data['temperature']['min']
    max_temp = data['temperature']['max']
    avg_temp = (data['temperature']['morning'] + data['temperature']['afternoon'] + data['temperature']['evening'] +
                data['temperature']['night']) / 4
    # Only humidity reading is afternoon
    humidity = data['humidity']['afternoon']
    return WeatherResponse(city=city, min_temp=min_temp, max_temp=max_temp, avg_temp=avg_temp, humidity=humidity)
