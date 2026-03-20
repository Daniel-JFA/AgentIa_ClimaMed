import requests
from datetime import datetime


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
MEDELLIN_NAME = "Medellin"
MEDELLIN_COUNTRY = "Colombia"


def geocode_medellin() -> dict:
    params = {"name": MEDELLIN_NAME, "count": 1, "language": "es", "format": "json"}
    response = requests.get(GEOCODING_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = data.get("results")
    if not results:
        raise ValueError("No encontré Medellin en la API de geocodificacion.")
    place = results[0]
    return {
        "name": place.get("name", MEDELLIN_NAME),
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "country": place.get("country", MEDELLIN_COUNTRY)
    }


def get_weather_forecast() -> dict:
    place = geocode_medellin()
    today = datetime.now().astimezone()
    params = {
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "timezone": "America/Bogota",
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
    }
    response = requests.get(FORECAST_URL, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()
    current = data.get("current", {})
    daily = data.get("daily", {})
    return {
        "city": place["name"],
        "country": place["country"],
        "latitude": place["latitude"],
        "longitude": place["longitude"],
        "today": today,
        "current": current,
        "daily": {
            "temperature_max": daily.get("temperature_2m_max", [None])[0],
            "temperature_min": daily.get("temperature_2m_min", [None])[0],
            "precipitation_sum": daily.get("precipitation_sum", [None])[0],
            "precipitation_probability_max": daily.get("precipitation_probability_max", [None])[0],
            "weather_code": daily.get("weather_code", [None])[0],
        }
    }
