# tests/test_weather.py
import pytest
from src.backend.weather import fetch_current_weather_by_city
import os

OPEN_WEATHER_KEY = os.getenv("OPEN_WEATHER_API_KEY")

@pytest.mark.skipif(not OPEN_WEATHER_KEY, reason="OPEN_WEATHER_API_KEY not set")
def test_fetch_weather():
    res = fetch_current_weather_by_city("London")
    assert "temp" in res
    assert "weather" in res