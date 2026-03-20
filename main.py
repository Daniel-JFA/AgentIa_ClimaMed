
from logistics_agent import agent as logistics_agent
from logistics_tool import get_response_mode, set_response_mode
from ollama_intent import OLLAMA_HOST, OLLAMA_MODEL, classify_intent, ollama_status
from simple_agent import agent as weather_agent
import unicodedata


def _normalize(text: str) -> str:
    # Normalize accents so intent matching works with/without tildes.
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


print("Agente IA (Clima + Logistica). Escribe 'salir' para terminar.")
print("Ejemplos:")
print("- clima medellin")
print("- repartidor mas cercano 6.2442 -75.5812")
print("- costo promedio por km")
print("- cuanto tarda 8.4 km carga 2")
print("- modo presentacion")
print("- modo tecnico")
print("- estado ollama")
print(f"Modo actual logistica: {get_response_mode()}")


while True:
    question = input("Pregunta: ").strip()

    if question.lower() == "salir":
        break

    lower_q = _normalize(question)

    if lower_q in {"modo presentacion", "modo tecnico"}:
        selected_mode = lower_q.split()[-1]
        set_response_mode(selected_mode)
        print(f"Agente: modo logistica cambiado a {selected_mode}.")
        continue

    if lower_q == "estado ollama":
        status = ollama_status()
        print(
            "Agente: "
            f"ollama={status}, host={OLLAMA_HOST}, modelo={OLLAMA_MODEL}"
        )
        continue

    logistics_keywords = [
        "repartidor", "pickup", "recogida", "prioritario", "pedido",
        "costo", "combustible", "mantenimiento", "km", "kilometro",
        "motocicleta", "moto", "flota", "eta", "tarda", "demora",
        "tiempo", "entrega", "trafico", "carga",
    ]

    weather_keywords = ["clima", "lluvia", "temperatura"]

    # Reglas directas primero para consultas comunes.
    if any(k in lower_q for k in logistics_keywords):
        response = logistics_agent(question)
    elif any(k in lower_q for k in weather_keywords):
        response = weather_agent(question)
    else:
        # Si no hay match claro, pedir clasificacion a Ollama.
        intent = classify_intent(question)
        if intent == "logistica":
            response = logistics_agent(question)
        elif intent == "clima":
            response = weather_agent(question)
        else:
            response = (
                "Puedo ayudarte en clima y logistica. "
                "Ejemplo: clima medellin / costo promedio por km / "
                "repartidor mas cercano 6.2442 -75.5812"
            )

    print("Agente:", response)
