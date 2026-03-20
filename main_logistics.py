from logistics_agent import agent
from logistics_tool import get_response_mode, set_response_mode
import unicodedata


def _normalize(text: str) -> str:
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


print("Agente de Logistica (BD Logistic). Escribe 'salir' para terminar.")
print("Ejemplos:")
print("- repartidor mas cercano 6.2442 -75.5812")
print("- costo promedio por km")
print("- cuanto tarda 8.4 km carga 2")
print("- modo presentacion")
print("- modo tecnico")
print(f"Modo actual: {get_response_mode()}")

while True:
    question = input("Pregunta: ")
    normalized_q = _normalize(question)

    if normalized_q == "salir":
        break

    if normalized_q in {"modo presentacion", "modo tecnico"}:
        selected_mode = normalized_q.split()[-1]
        set_response_mode(selected_mode)
        print(f"Agente: modo cambiado a {selected_mode}.")
        continue

    response = agent(question)
    print("Agente:", response)
