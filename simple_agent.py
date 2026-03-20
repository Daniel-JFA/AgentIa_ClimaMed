
from weather_tool import get_weather

def agent(question: str):
    question = question.lower()

    if "clima" in question or "lluvia" in question or "temperatura" in question:
        words = question.split()
        city = words[-1]
        result = get_weather(city)
        return result

    return "Puedo ayudarte a consultar el clima de una ciudad."
