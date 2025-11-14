# src/backend/weather.py
import os
import requests
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")

def fetch_current_weather_by_city(city: str, units: str = "metric") -> Dict:
    """
    Fetch current weather from OpenWeatherMap (Current Weather API).
    Returns parsed JSON.
    """
    if not OPEN_WEATHER_KEY:
        raise ValueError("OPEN_WEATHER_API_KEY not set in environment")

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPEN_WEATHER_KEY,
        "units": units
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # Normalized minimal structure:
    return {
        "city": data.get("name"),
        "weather": data["weather"][0]["description"] if data.get("weather") else None,
        "temp": data["main"]["temp"] if data.get("main") else None,
        "feels_like": data["main"].get("feels_like") if data.get("main") else None,
        "humidity": data["main"].get("humidity") if data.get("main") else None,
        "raw": data
    }