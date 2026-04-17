import os
import sys
import unicodedata

import requests

try:
    from tools.weather_api import get_weather_forecast
except ModuleNotFoundError:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if base_dir not in sys.path:
        sys.path.insert(0, base_dir)
    from tools.weather_api import get_weather_forecast


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "qwen3-vl:8b")
SUPPORTED_CITY = "medellin"
context = {"pending_weather_question": None, "zone": None}


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
        "clima", "lluvia", "llover", "llueve", "temperatura",
        "tiempo", "sombrilla", "pronostico", "humedad", "viento",
        "sol", "soleado", "nublado", "nubes",
    ]
    q = _normalize(question)
    return any(word in q for word in keywords)


def extract_city(question: str) -> str:
    known_cities = ["medellin", "bogota", "cali", "barranquilla", "cartagena"]
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
    zone_context = {
        "poblado": "El Poblado es una zona premium, urbana y comercial.",
        "laureles": "Laureles es residencial y comercial. Clima variable.",
        "estadio": "Zona del Estadio es comercial. Muy transitada.",
        "belen": "Belén es residencial, ubicada en zona montañosa.",
        "envigado": "Envigado es zona sur; clima más frío.",
        "sabaneta": "Sabaneta es zona sur; temperatura baja.",
        "robledo": "Robledo es zona norte residencial; clima fresco.",
        "arvi": "Arví es zona montañosa norte; clima más frío y lluvioso.",
        "castilla": "Castilla es zona central; muy transitada.",
        "santa elena": "Santa Elena es zona centroeste; residencial.",
        "moravia": "Moravia es zona norte, residencial.",
    }
    for key, note in zone_context.items():
        if key in z:
            return note
    return f"Zona: {zone}. Te ayudaré con recomendaciones según el clima local."


def extract_zone(question: str) -> str | None:
    known_zones = [
        "poblado", "laureles", "estadio", "belen", "envigado",
        "sabaneta", "robledo", "arví", "arvi", "castilla",
        "santa elena", "moravia", "altos", "palmitas",
    ]
    q = _normalize(question)
    for zone in known_zones:
        if zone in q:
            return zone
    return None


def _detect_intent(question: str) -> str:
    q = _normalize(question)
    if any(k in q for k in ["humedad"]):
        return "humidity"
    if any(k in q for k in ["viento", "ventoso"]):
        return "wind"
    if any(k in q for k in ["temperatura", "frio", "calor"]):
        return "temperature"
    if any(k in q for k in ["lluvia", "llover", "llueve", "sombrilla", "precipitacion"]):
        return "rain"
    return "general"


def build_prompt(question: str, weather: dict, zone: str | None) -> str:
    current = weather["current"]
    daily = weather["daily"]
    today = weather["today"]
    zone_text = zone if zone else "No especificada"
    zone_note = zone_context_note(zone) if zone else "No hay zona especificada."
    return f"""Eres un agente meteorologico util, claro y breve.

Pregunta del usuario:
Fecha: {today.strftime("%Y-%m-%d")}
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
Ciudad fija del agente: Medellin
Zona/Barrio: {zone_text}
Nota contextual: {zone_note}

Instrucciones:
- Responde en espanol.
- No inventes datos.
- Se breve, maximo 4 lineas.
- La primera linea debe empezar con: Fecha: {today.strftime("%Y-%m-%d")}
- Explica si parece que va a llover o no.
- Si aplica, recomienda sombrilla, chaqueta ligera o precaucion al salir.
"""


def _fallback_answer(question: str, weather: dict, zone: str | None) -> str:
    intent = _detect_intent(question)
    today = weather["today"]
    city = weather["city"]
    current = weather["current"]
    daily = weather["daily"]

    temp = current.get("temperature_2m")
    feels = current.get("apparent_temperature")
    humidity = current.get("relative_humidity_2m")
    wind = current.get("wind_speed_10m")
    temp_max = daily.get("temperature_max")
    temp_min = daily.get("temperature_min")
    precip_now = current.get("precipitation")
    precip_total = daily.get("precipitation_sum")
    rain_prob = weather["daily"].get("precipitation_probability_max")

    if intent == "humidity":
        focus_line = (
            f"En {city}, humedad actual: {humidity}%. "
            f"Temperatura: {temp} C (sensacion {feels} C)."
        )
        recommendation = (
            "Humedad alta: ropa ligera y ventilada puede ser mas comoda."
            if (humidity or 0) >= 75
            else "Humedad moderada: condiciones relativamente comodas."
        )
    elif intent == "wind":
        focus_line = (
            f"En {city}, viento actual: {wind} km/h. "
            f"Con {temp} C de temperatura y {rain_prob}% de lluvia probable."
        )
        recommendation = (
            "Viento fuerte: evita paraguas fragiles y asegura objetos sueltos."
            if (wind or 0) > 20
            else "Viento suave a moderado: movilidad normal en la zona."
        )
    elif intent == "temperature":
        focus_line = (
            f"En {city}, temperatura actual: {temp} C (sensacion {feels} C). "
            f"Rango de hoy: min {temp_min} C, max {temp_max} C."
        )
        if temp is not None and temp < 15:
            recommendation = "Se siente fresco: lleva chaqueta ligera."
        elif temp is not None and temp > 28:
            recommendation = "Temperatura alta: hidratarse y protegerse del sol."
        else:
            recommendation = "Temperatura templada: ropa comoda recomendada."
    elif intent == "rain":
        focus_line = (
            f"En {city}, probabilidad maxima de lluvia: {rain_prob}%. "
            f"Precipitacion actual: {precip_now}; total esperado hoy: {precip_total}."
        )
        if (rain_prob or 0) >= 60:
            recommendation = "Alta probabilidad de lluvia: lleva sombrilla o impermeable."
        elif (rain_prob or 0) >= 40:
            recommendation = "Posible lluvia: sombrilla recomendada."
        else:
            recommendation = "Baja probabilidad de lluvia: no parece necesario paraguas."
    else:
        focus_line = (
            f"En {city}: {temp} C, sensacion {feels} C, "
            f"humedad {humidity}% y lluvia probable {rain_prob}%."
        )
        recommendation = "Resumen general del clima para planear tus salidas hoy."

    zone_note = f"\nZona: {zone}. {zone_context_note(zone)}" if zone else ""

    return (
        f"Fecha: {today.strftime('%Y-%m-%d')}. "
        f"{focus_line} "
        f"{recommendation}{zone_note}"
    )


def answer_weather(question: str, zone: str | None) -> str:
    weather = get_weather_forecast()
    prompt = build_prompt(question, weather, zone)
    llm_answer = ask_ollama(prompt)
    if llm_answer:
        today_text = weather["today"].strftime("%Y-%m-%d")
        if today_text not in llm_answer:
            return f"Fecha: {today_text}\n{llm_answer}"
        return llm_answer
    return _fallback_answer(question, weather, zone)


def agent(question: str) -> str:
    q = question.strip()
    city = extract_city(q)
    detected_zone = extract_zone(q)

    if detected_zone:
        context["zone"] = detected_zone
    elif city == SUPPORTED_CITY:
        # Si menciona Medellin pero no zona, no arrastres una zona vieja.
        context["zone"] = None

    if city and city != SUPPORTED_CITY:
        return "Este agente solo consulta clima para Medellin. Prueba con algo como: va a llover hoy en Medellin?"

    if context["pending_weather_question"]:
        if looks_like_zone_answer(q):
            context["zone"] = q
            original_question = context["pending_weather_question"]
            context["pending_weather_question"] = None
            return answer_weather(original_question, context["zone"])

    if is_weather_question(q):
        return answer_weather(q, context["zone"])

    return "Puedo ayudarte con clima en Medellin. Ejemplo: va a llover hoy en Medellin?"


def main() -> None:
    print("Agente de clima. Escribe 'salir' para terminar.\n")
    while True:
        question = input("Tu: ").strip()
        if _normalize(question) == "salir":
            print("Agente: Hasta luego.")
            break
        try:
            answer = agent(question)
            print(f"\nAgente: {answer}\n")
        except Exception as exc:
            print(f"\nAgente: Error: {exc}\n")


if __name__ == "__main__":
    main()
