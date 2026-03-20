import os
import sys
import unicodedata

import requests

try:
    from tools.weather_api import get_weather_forecast
except ModuleNotFoundError:
    # Soporta ejecucion directa: python agents/weather_agent_real.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    from tools.weather_api import get_weather_forecast


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "llama3")

context = {"pending_weather_question": None, "city": None, "zone": None}


def _normalize(text: str) -> str:
    lowered = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", lowered)
        if unicodedata.category(c) != "Mn"
    )


def ask_ollama(prompt: str) -> str | None:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": MODEL_NAME, "prompt": prompt, "stream": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json().get("response", "").strip() or None
    except requests.RequestException:
        return None


def is_weather_question(question: str) -> bool:
    keywords = [
        "clima",
        "lluvia",
        "temperatura",
        "tiempo",
        "sombrilla",
        "pronostico",
    ]
    q = _normalize(question)
    return any(word in q for word in keywords)


def extract_city(question: str) -> str:
    known_cities = [
        "medellin",
        "bogota",
        "cali",
        "barranquilla",
        "cartagena",
    ]
    q = _normalize(question)
    for city in known_cities:
        if city in q:
            return city
    return ""


def looks_like_zone_answer(question: str) -> bool:
    q = _normalize(question)
    if len(q) < 2:
        return False
    return not is_weather_question(q)


def zone_context_note(zone: str) -> str:
    z = _normalize(zone)
    if "poblado" in z:
        return "El Poblado es una zona urbana de Medellin; conviene considerar lluvia y movilidad."
    if "laureles" in z or "estadio" in z:
        return "Laureles/Estadio es una zona urbana; una sombrilla o chaqueta ligera puede ser util."
    if "belen" in z:
        return "Belen es una zona urbana; es util salir prevenido si aumenta la probabilidad de lluvia."
    return f"La zona indicada es {zone}; usa esta referencia para personalizar la recomendacion."


def build_prompt(question: str, weather: dict, zone: str | None) -> str:
    current = weather["current"]
    daily = weather["daily"]
    zone_text = zone if zone else "No especificada"
    zone_note = zone_context_note(zone) if zone else "No hay zona especificada."
    return f"""
Eres un agente meteorologico util, claro y breve.

Pregunta del usuario:
{question}

Datos reales del clima consultados por API:
Ciudad: {weather['city']}, {weather['country']}
Temperatura actual: {current.get('temperature_2m')} C
Sensacion termica: {current.get('apparent_temperature')} C
Humedad relativa: {current.get('relative_humidity_2m')} %
Precipitacion actual: {current.get('precipitation')}
Lluvia actual: {current.get('rain')}
Viento: {current.get('wind_speed_10m')} km/h

Pronostico de hoy:
Temperatura maxima: {daily.get('temperature_max')} C
Temperatura minima: {daily.get('temperature_min')} C
Precipitacion total esperada: {daily.get('precipitation_sum')}
Probabilidad maxima de precipitacion: {daily.get('precipitation_probability_max')} %

Contexto del usuario:
Zona/Barrio: {zone_text}
Nota contextual: {zone_note}

Instrucciones:
- Responde en espanol.
- No inventes datos.
- Se breve, maximo 4 lineas.
- Explica si parece que va a llover o no.
- Si aplica, recomienda sombrilla, chaqueta ligera o precaucion al salir.
- Usa el barrio o zona solo como contexto de recomendacion.
"""


def _fallback_answer(weather: dict, zone: str | None) -> str:
    city = weather["city"]
    temp = weather["current"].get("temperature_2m")
    rain_prob = weather["daily"].get("precipitation_probability_max")
    zone_note = f" Zona: {zone}." if zone else ""
    recommendation = "Lleva sombrilla." if (rain_prob or 0) >= 40 else "No parece necesario llevar sombrilla."
    return (
        f"En {city} la temperatura actual es {temp} C y la probabilidad maxima de lluvia hoy es {rain_prob}%."
        f" {recommendation}{zone_note}"
    )


def answer_weather(question: str, city: str, zone: str | None) -> str:
    weather = get_weather_forecast(city)
    prompt = build_prompt(question, weather, zone)
    llm_answer = ask_ollama(prompt)
    if llm_answer:
        return llm_answer
    return _fallback_answer(weather, zone)


def agent(question: str) -> str:
    q = question.strip()

    if context["pending_weather_question"] and context["city"] == "medellin":
        if looks_like_zone_answer(q):
            context["zone"] = q
            original_question = context["pending_weather_question"]
            context["pending_weather_question"] = None
            return answer_weather(original_question, context["city"], context["zone"])

    if is_weather_question(q):
        city = extract_city(q)
        if city:
            context["city"] = city
        if not context["city"]:
            return "No detecte la ciudad. Prueba con algo como: va a llover hoy en Medellin?"
        if context["city"] == "medellin" and not context["zone"]:
            context["pending_weather_question"] = q
            return "Estas en Medellin. En que barrio o zona estas ubicado?"
        return answer_weather(q, context["city"], context["zone"])

    return "Puedo ayudarte con clima, lluvia, temperatura y pronostico. Ejemplo: clima medellin"


def main() -> None:
    print("Agente de clima real con Ollama. Escribe 'salir' para terminar.\n")
    while True:
        question = input("Tu: ").strip()
        if _normalize(question) == "salir":
            print("Agente: Hasta luego.")
            break
        try:
            answer = agent(question)
            print(f"\nAgente: {answer}\n")
        except Exception as exc:
            print(f"\nAgente: Ocurrio un error: {exc}\n")


if __name__ == "__main__":
    main()
