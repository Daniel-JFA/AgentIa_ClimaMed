# Documentacion de la API

Este proyecto usa principalmente la API de Open-Meteo para consultar el clima real de Medellin.
De forma opcional, tambien usa la API local de Ollama para redactar respuestas mas naturales.

## 1. API principal: Open-Meteo

### 1.1 Geocodificacion

Se usa para obtener las coordenadas de Medellin antes de consultar el pronostico.

- Metodo: `GET`
- Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
- Uso en el proyecto: [`Clase2/06_codigo/tools/weather_api.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/tools/weather_api.py#L8)

#### Parametros usados

- `name=Medellin`
- `count=1`
- `language=es`
- `format=json`

#### Ejemplo

```bash
curl "https://geocoding-api.open-meteo.com/v1/search?name=Medellin&count=1&language=es&format=json"
```

#### Campos relevantes de respuesta

- `results[0].name`
- `results[0].latitude`
- `results[0].longitude`
- `results[0].country`

### 1.2 Pronostico del clima

Se usa para obtener las condiciones actuales y el resumen diario del clima de Medellin.

- Metodo: `GET`
- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Uso en el proyecto: [`Clase2/06_codigo/tools/weather_api.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/tools/weather_api.py#L24)

#### Parametros usados por el agente

- `latitude`
- `longitude`
- `timezone=America/Bogota`
- `current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m`
- `daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max`

#### Ejemplo

```bash
curl "https://api.open-meteo.com/v1/forecast?latitude=6.25184&longitude=-75.56359&timezone=America/Bogota&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max"
```

#### Campos que consume el proyecto

En `current`:

- `temperature_2m`
- `relative_humidity_2m`
- `apparent_temperature`
- `precipitation`
- `rain`
- `weather_code`
- `wind_speed_10m`

En `daily`:

- `temperature_2m_max`
- `temperature_2m_min`
- `precipitation_sum`
- `precipitation_probability_max`
- `weather_code`

## 2. Flujo de consumo en este proyecto

1. El usuario pregunta por el clima en Medellin.
2. El agente resuelve las coordenadas de Medellin con la API de geocodificacion.
3. Con esas coordenadas consulta la API de pronostico.
4. El sistema arma una respuesta con fecha actual, temperatura y probabilidad de lluvia.
5. Si Ollama esta disponible, reescribe la respuesta en lenguaje mas natural.

Archivos clave:

- [`main.py`](/home/djfa/Dev/ai/agente_clima_medellin/main.py#L1)
- [`Clase2/06_codigo/agents/weather_agent_real.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/agents/weather_agent_real.py#L1)
- [`Clase2/06_codigo/tools/weather_api.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/tools/weather_api.py#L1)

## 3. API opcional: Ollama

El proyecto usa Ollama solo para generar una respuesta mas natural. Si Ollama falla, el agente sigue respondiendo con datos reales de Open-Meteo.

- Metodo: `POST`
- Endpoint local: `http://localhost:11434/api/generate`
- Uso en el proyecto: [`Clase2/06_codigo/agents/weather_agent_real.py`](/home/djfa/Dev/ai/agente_clima_medellin/Clase2/06_codigo/agents/weather_agent_real.py#L31)

#### Body usado

```json
{
  "model": "llama3",
  "prompt": "Tu prompt aqui",
  "stream": false
}
```

#### Campos de respuesta usados

- `response`

## 4. Autenticacion

- Open-Meteo: no requiere autenticacion para este uso segun su documentacion publica.
- Ollama local: no requiere autenticacion cuando corre localmente en `localhost`.

## 5. Fuentes oficiales

- Open-Meteo Geocoding API: https://open-meteo.com/en/docs/geocoding-api
- Open-Meteo Weather Forecast API: https://open-meteo.com/en/docs
- Ollama API Introduction: https://docs.ollama.com/api/introduction
- Ollama Generate API: https://docs.ollama.com/api/generate
