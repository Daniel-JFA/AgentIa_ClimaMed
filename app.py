#!/usr/bin/env python3
"""
Servidor Flask para el Agente de Clima de Medellín.
Proporciona una interfaz web moderna y interactiva.

Uso:
    python app.py

Luego abre http://localhost:5000 en tu navegador.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Setup de ruta para importar el agente
BASE_DIR = Path(__file__).resolve().parent
WEATHER_DIR = BASE_DIR / "Clase2" / "06_codigo"
weather_dir_str = str(WEATHER_DIR)
if weather_dir_str not in sys.path:
    sys.path.insert(0, weather_dir_str)

from agents.weather_agent_real import agent as weather_agent

# Crear app Flask
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Configuración
app.config["JSON_SORT_KEYS"] = False


@app.route("/")
def index():
    """Renderiza la página principal."""
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask_weather():
    """
    Endpoint para consultar el clima.
    
    Request JSON:
    {
        "question": "clima medellin"
    }
    
    Response JSON:
    {
        "success": true,
        "question": "clima medellin",
        "response": "Fecha: 2026-04-17...",
        "timestamp": "2026-04-17 14:30:45"
    }
    """
    try:
        data = request.get_json()
        
        if not data or "question" not in data:
            return jsonify({
                "success": False,
                "error": "Campo 'question' requerido"
            }), 400
        
        question = data["question"].strip()
        
        if not question:
            return jsonify({
                "success": False,
                "error": "La pregunta no puede estar vacía"
            }), 400
        
        # Llamar al agente
        response = weather_agent(question)
        
        return jsonify({
            "success": True,
            "question": question,
            "response": response,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    
    except Exception as exc:
        return jsonify({
            "success": False,
            "error": f"Error: {str(exc)}"
        }), 500


@app.route("/api/examples", methods=["GET"])
def get_examples():
    """Devuelve ejemplos de preguntas para la interfaz."""
    examples = [
        "clima medellin",
        "va a llover hoy?",
        "temperatura en el poblado",
        "hace frio en laureles?",
        "clima en belen",
        "pronostico hoy",
    ]
    return jsonify({
        "success": True,
        "examples": examples
    }), 200


@app.route("/api/zones", methods=["GET"])
def get_zones():
    """Devuelve las zonas soportadas."""
    zones = [
        "Poblado",
        "Laureles",
        "Estadio",
        "Belén",
        "Envigado",
        "Sabaneta",
        "Robledo",
        "Arví",
        "Castilla",
        "Santa Elena",
        "Moravia"
    ]
    return jsonify({
        "success": True,
        "zones": zones
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "Agente de Clima para Medellín",
        "version": "1.0"
    }), 200


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  AGENTE DE IA PARA CLIMA EN MEDELLÍN - WEB SERVER")
    print("=" * 70)
    print("\n🚀 Servidor iniciado en http://localhost:5000")
    print("📊 Abre tu navegador y accede a http://localhost:5000\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
