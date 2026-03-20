# Agente de Clima para Medellin

Agente de linea de comandos en Python para consultar el clima real de Medellin.

El proyecto consulta Open-Meteo en cada solicitud y, si Ollama esta disponible localmente, usa un modelo LLM para redactar una respuesta mas natural. Si Ollama no responde, el agente sigue funcionando con un fallback basado en datos reales.

## Que hace

- Responde preguntas de clima para Medellin.
- Usa datos reales de APIs externas.
- Incluye la fecha actual en la respuesta.
- Puede personalizar la recomendacion si detecta una zona como `poblado`, `laureles` o `belen`.
- Rechaza otras ciudades para mantener el flujo enfocado solo en Medellin.

## Herramienta de IA usada

Este proyecto no usa un framework de agentes como LangChain, CrewAI o AutoGen.

La implementacion del agente esta hecha de forma manual en Python, y la herramienta de IA generativa que estamos usando es:

- `Ollama`, via `POST /api/generate`, para transformar los datos del clima en una respuesta natural.

La fuente real de informacion meteorologica no es el modelo, sino:

- `Open-Meteo Geocoding API`
- `Open-Meteo Forecast API`

En otras palabras:

- `Open-Meteo` aporta los datos.
- `Ollama` aporta redaccion natural.
- `Python` orquesta el agente.

## Arquitectura

Archivos principales:

- [`main.py`](/home/djfa/Dev/ai/agente_clima_medellin/main.py)
- [`Clase2/06_codigo/agents/weather_agent_real.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/agents/weather_agent_real.py)
- [`Clase2/06_codigo/tools/weather_api.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/tools/weather_api.py)
- [`API.md`](/home/djfa/Dev/ai/agente_clima_medellin/API.md)

Flujo:

1. El usuario escribe una pregunta.
2. `main.py` envia la pregunta al agente de clima.
3. El agente valida que la consulta sea para Medellin.
4. `weather_api.py` consulta Open-Meteo.
5. El agente arma un prompt con fecha y datos reales.
6. Si Ollama responde, se usa esa salida.
7. Si Ollama no responde, se devuelve un fallback con los datos de Open-Meteo.

## APIs consumidas

### 1. Open-Meteo Geocoding API

Se usa para resolver las coordenadas de Medellin.

- Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
- Metodo: `GET`

### 2. Open-Meteo Forecast API

Se usa para obtener condiciones actuales y pronostico diario.

- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Metodo: `GET`

### 3. Ollama Generate API

Se usa de forma opcional para redactar la respuesta final.

- Endpoint local: `http://localhost:11434/api/generate`
- Metodo: `POST`

La documentacion ampliada esta en:

- [`API.md`](/home/djfa/Dev/ai/agente_clima_medellin/API.md)

## Requisitos

- Python 3
- `requests`
- Conexion a internet para Open-Meteo
- Ollama opcional si quieres salida mas natural

## Ejecucion

Desde la raiz del proyecto:

```bash
python main.py
```

Ejemplos:

```text
clima medellin
va a llover hoy en medellin
temperatura hoy en medellin
necesito sombrilla en medellin
```

## Comportamiento esperado

- Si preguntas por Medellin, responde con clima real.
- Si no indicas ciudad, asume Medellin.
- Si preguntas por otra ciudad, el agente lo rechaza.
- La respuesta incluye la fecha actual.

## Ejemplo de salida

```text
Fecha: 2026-03-20. En Medellin la temperatura actual es 22.6 C y la probabilidad maxima de lluvia hoy es 15%. No parece necesario llevar sombrilla.
```

## Notas

- El agente consulta la API en cada solicitud; no trabaja con datos hardcodeados.
- Ollama es opcional. Si no esta levantado, el agente sigue respondiendo.
- El proyecto esta enfocado en un solo caso de uso: clima para Medellin.

## Referencias oficiales

- Open-Meteo Geocoding API: https://open-meteo.com/en/docs/geocoding-api
- Open-Meteo Forecast API: https://open-meteo.com/en/docs
- Ollama API: https://docs.ollama.com/api/generate
