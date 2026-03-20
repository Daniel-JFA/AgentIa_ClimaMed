import sys
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
WEATHER_DIR = BASE_DIR / "Clase2" / "06_codigo"

weather_dir_str = str(WEATHER_DIR)
if weather_dir_str not in sys.path:
    sys.path.insert(0, weather_dir_str)

from agents.weather_agent_real import agent as weather_agent


def _normalize(text: str) -> str:
    text = text.lower().strip()
    return "".join(
        c for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


def route_question(question: str) -> str:
    return weather_agent(question)


def main() -> None:
    print("Agente IA de Clima para Medellin. Escribe 'salir' para terminar.")
    print("Ejemplos:")
    print("- clima medellin")
    print("- va a llover hoy en medellin")
    print("- temperatura hoy en medellin")
    print("- necesito sombrilla en medellin")

    while True:
        question = input("Pregunta: ").strip()

        if _normalize(question) == "salir":
            break

        try:
            response = route_question(question)
        except Exception as exc:
            response = f"Ocurrio un error: {exc}"

        print("Agente:", response)


if __name__ == "__main__":
    main()
