from fastapi import FastAPI, Request, Query
from pydantic import BaseModel
from typing import List, Dict, Any
import requests


app = FastAPI()

API_KEY = "4f3aca5105ef44cd1dddab94f8fda078"
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather"


async def get_weather(req_json):
    city = req_json['queryResult']["parameters"]["geo-city"]
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(WEATHER_URL, params=params)
    data = response.json()

    if response.status_code != 200:
        return {"fulfillmentText": f"Error: {data.get('message', 'Failed to get weather data')}"}

    weather = {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }

    fulfillment_text = (
        f"The current weather in {weather['city']} is {weather['description']} with a temperature of "
        f"{weather['temperature']}°C, humidity of {weather['humidity']}%, and a wind speed of "
        f"{weather['wind_speed']} m/s."
    )

    return {"fulfillmentText": fulfillment_text}

