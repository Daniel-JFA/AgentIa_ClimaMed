import json
import os
import urllib.error
import urllib.request
from typing import Optional


OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def _post_json(path: str, payload: dict, timeout: float = 4.0) -> Optional[dict]:
    url = f"{OLLAMA_HOST}{path}"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def _get_json(path: str, timeout: float = 2.0) -> Optional[dict]:
    url = f"{OLLAMA_HOST}{path}"
    req = urllib.request.Request(url, method="GET")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def ollama_status() -> str:
    tags = _get_json("/api/tags")
    if not tags:
        return "desconectado"

    models = tags.get("models", [])
    if not models:
        return "conectado_sin_modelos"

    loaded = [m.get("name", "") for m in models if m.get("name")]
    if OLLAMA_MODEL in loaded:
        return "conectado_modelo_ok"
    return "conectado_modelo_no_encontrado"


def classify_intent(question: str) -> Optional[str]:
    """Return one of: logistica, clima, otro, or None if Ollama unavailable."""
    prompt = (
        "Clasifica la pregunta del usuario en UNA sola etiqueta exacta: "
        "LOGISTICA, CLIMA u OTRO. "
        "Responde solo la etiqueta, sin explicacion.\n"
        f"Pregunta: {question}"
    )

    data = _post_json(
        "/api/generate",
        {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0},
        },
    )
    if not data:
        return None

    text = str(data.get("response", "")).strip().lower()
    if "logistica" in text:
        return "logistica"
    if "clima" in text:
        return "clima"
    if "otro" in text:
        return "otro"
    return "otro"
