
def get_weather(city: str) -> str:
    weather_data = {
        "medellin": "25°C, parcialmente nublado con posibilidad de lluvia",
        "bogota": "18°C, lluvioso",
        "cali": "30°C, soleado"
    }

    city = city.lower()

    if city in weather_data:
        return f"El clima en {city} es {weather_data[city]}"
    else:
        return "No tengo información del clima para esa ciudad."
