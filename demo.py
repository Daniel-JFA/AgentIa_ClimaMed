#!/usr/bin/env python3
"""
Script de demostración del Agente de Clima para Medellín.
Ejecuta automáticamente varios ejemplos para la presentación en clase.

Uso:
    python demo.py
"""

import sys
import time
from pathlib import Path

# Setup de ruta
BASE_DIR = Path(__file__).resolve().parent
WEATHER_DIR = BASE_DIR / "Clase2" / "06_codigo"
weather_dir_str = str(WEATHER_DIR)
if weather_dir_str not in sys.path:
    sys.path.insert(0, weather_dir_str)

from agents.weather_agent_real import agent as weather_agent


def print_section(title: str) -> None:
    """Imprime un título de sección."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_question(question: str, delay: float = 1.0) -> None:
    """Ejecuta una pregunta de demostración."""
    print(f"\n👤 Usuario: {question}")
    time.sleep(delay)
    try:
        response = weather_agent(question)
        print(f"🤖 Agente: {response}")
    except Exception as exc:
        print(f"❌ Error: {exc}")
    time.sleep(0.5)


def main() -> None:
    print("\n")
    print("╔═══════════════════════════════════════════════════════════════════╗")
    print("║          DEMOSTRACIÓN: AGENTE DE IA PARA CLIMA EN MEDELLÍN        ║")
    print("╚═══════════════════════════════════════════════════════════════════╝")

    # 1. Casos básicos
    print_section("1. CASOS BÁSICOS - Preguntas simples sobre clima")
    demo_question("clima medellin", delay=1.5)
    demo_question("va a llover hoy?", delay=1.5)
    demo_question("temperatura en medellin?", delay=1.5)

    # 2. Detección de zonas
    print_section("2. PERSONALIZACIÓN POR ZONA - El agente reconoce barrios")
    demo_question("clima en el poblado", delay=1.5)
    demo_question("hace frio en laureles?", delay=1.5)
    demo_question("va a llover en belen?", delay=1.5)

    # 3. Validación de ciudades
    print_section("3. VALIDACIÓN - Solo responde sobre Medellín")
    demo_question("clima en bogota", delay=1.5)
    demo_question("temperatura en cali?", delay=1.5)

    # 4. Casos edge
    print_section("4. CASOS EDGE - Preguntas inusuales")
    demo_question("hola", delay=1.0)
    demo_question("necesito sombrilla en medellin", delay=1.5)

    # Resumen
    print_section("RESUMEN DE FUNCIONALIDADES")
    print("""
✅ Responde preguntas sobre clima usando datos REALES de APIs externas
✅ Personaliza respuestas según la zona/barrio de Medellín
✅ Valida que las consultas sean para Medellín
✅ Usa Ollama (si disponible) para respuestas naturales
✅ Fallback automático si Ollama no está disponible
✅ Fácil de usar desde línea de comandos

🏗️  ARQUITECTURA:
   - Python: Orquestación del agente
   - Open-Meteo: Datos meteorológicos reales
   - Ollama: Redacción natural (opcional)
   - No usa frameworks como LangChain

📊 ZONAS SOPORTADAS:
   Poblado, Laureles, Estadio, Belén, Envigado, Sabaneta,
   Robledo, Arví, Castilla, Santa Elena, Moravia

🚀 EJECUTAR INTERACTIVO:
   python main.py
    """)

    print("\n" + "=" * 70)
    print("            ✨ Fin de la demostración. Gracias por ver. ✨")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
