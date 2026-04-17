# Agente de Clima para Medellín 🌤️

Agente de línea de comandos en Python para consultar el clima real de Medellín con respuestas naturales.

El proyecto consulta **Open-Meteo** en cada solicitud y, si **Ollama** está disponible localmente, usa un modelo LLM para redactar una respuesta más natural. Si Ollama no responde, el agente sigue funcionando perfectamente con un fallback inteligente basado en datos reales.

## ¿Qué hace?

- ✅ Responde preguntas de clima para Medellín en español.
- ✅ Usa datos **reales** de APIs externas (sin alucinaciones).
- ✅ Incluye la fecha actual en cada respuesta.
- ✅ Personaliza recomendaciones por zona/barrio (Poblado, Laureles, Belén, etc.).
- ✅ Rechaza otras ciudades para mantener el flujo enfocado en Medellín.
- ✅ Funciona **con o sin Ollama** (degradación elegante).

## Herramientas de IA

Este proyecto **no usa frameworks** como LangChain, CrewAI o AutoGen.

La implementación es manual en Python:

| Componente | Rol |
|-----------|-----|
| **Python** | Orquestación del agente |
| **Ollama** | (Opcional) Redacción natural con LLM local |
| **Open-Meteo APIs** | Fuente de datos meteorológicos reales |

En otras palabras:
- `Open-Meteo` → aporta los datos
- `Ollama` → aporta redacción natural (si está disponible)
- `Python` → orquesta el agente

## Arquitectura

```
Usuario (CLI)
    ↓
main.py (loop de preguntas)
    ↓
weather_agent_real.py (routing, detección de ciudad/zona)
    ↓
weather_api.py (APIs externas)
    ├→ Open-Meteo Geocoding (obtener coordenadas)
    └→ Open-Meteo Forecast (datos climáticos)
    ↓
ask_ollama() → Respuesta natural (si disponible)
    ↓ (fallback si Ollama no responde)
_fallback_answer() → Respuesta estructurada con datos reales
```

## Zonas soportadas

El agente reconoce y personaliza recomendaciones para estas zonas de Medellín:

| Zona | Características |
|------|-----------------|
| **El Poblado** | Zona premium urbana; lluvia afecta actividades al aire libre |
| **Laureles** | Residencial y comercial; clima variable |
| **Estadio** | Zona muy transitada; sombrilla útil |
| **Belén** | Residencial montañoso; mayor exposición al clima |
| **Envigado** | Zona sur; temperatura más baja |
| **Sabaneta** | Zona sur; temperatura baja en lluvia |
| **Robledo** | Zona norte residencial; clima fresco |
| **Arví** | Montañosa; clima más frío y lluvioso |
| **Castilla, Santa Elena, Moravia** | Zonas adicionales soportadas |

## APIs consumidas

### 1. Open-Meteo Geocoding API
Resuelve coordenadas de Medellín.
- Endpoint: `https://geocoding-api.open-meteo.com/v1/search`
- Método: `GET`

### 2. Open-Meteo Forecast API
Datos de clima actual y pronóstico del día.
- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Método: `GET`
- Incluye: temperatura, humedad, precipitación, viento, código meteorológico

### 3. Ollama Generate API (opcional)
Redacta respuestas naturales con LLM local.
- Endpoint: `http://localhost:11434/api/generate`
- Método: `POST`
- **Nota:** El agente funciona sin esto (ve fallback abajo)

Documentación completa: [`API.md`](API.md)

## Requisitos

- Python 3.7+
- `requests` (HTTP client)
- Conexión a internet (para Open-Meteo)
- Ollama (recomendado para mejores respuestas, pero opcional)

## Instalación

```bash
# Clonar o descargar el proyecto
cd agente_clima_medellin

# Crear entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r Clase2/06_codigo/requirements.txt
```

## Ejecución

```bash
python main.py
```

### Ejemplos de consultas

```text
clima medellin
va a llover hoy en medellin?
temperatura hoy en medellin
necesito sombrilla en medellin
clima en el poblado
pronostico en laureles
temperature en belen
```

## Comportamiento

### Con Ollama disponible (respuesta óptima)
```
Pregunta: va a llover hoy en medellin?

Agente: Fecha: 2026-04-17
En Medellín, la probabilidad de lluvia es del 55%. Te recomiendo llevar sombrilla.
La temperatura ronda 22°C, así que puedes ir con ropa ligera.
```

### Sin Ollama (fallback inteligente)
```
Pregunta: va a llover hoy en medellin?

Agente: Fecha: 2026-04-17. En Medellín: 22°C, sensación de 21°C. 
Lluvia esperada: 55%. Posible lluvia; sombrilla recomendada.
```

## Características avanzadas

### 1. Validación de ciudades
Solo responde sobre **Medellín**. Rechaza otras ciudades:
```
Pregunta: clima en bogota?
Agente: Este agente solo consulta clima para Medellín...
```

### 2. Detección automática de zonas
Identifica zonas en la pregunta y personaliza respuestas:
```
Pregunta: hace frio en el poblado?
Agente: [Personaliza con contexto del Poblado]
```

### 3. Contexto conversacional persistente
Recuerda la zona seleccionada en la sesión actual:
```
Pregunta: clima en laureles
[Agente recuerda: zona = "laureles"]

Pregunta: va a llover?
[Usa "laureles" como contexto]
```

### 4. Manejo robusto de errores
- APIs caídas: mensaje claro al usuario
- Ollama no responde: usa fallback automático
- Preguntas inválidas: sugiere ejemplos

## Configuración

Variables de entorno (opcionales):
```bash
export OLLAMA_URL="http://localhost:11434/api/generate"
export OLLAMA_MODEL="llama3"
```

Por defecto usa estos valores si no están definidas.

## Archivos principales

- [main.py](main.py) - Punto de entrada
- [Clase2/06_codigo/agents/weather_agent_real.py](Clase2/06_codigo/agents/weather_agent_real.py) - Lógica del agente
- [Clase2/06_codigo/tools/weather_api.py](Clase2/06_codigo/tools/weather_api.py) - Consumo de APIs
- [API.md](API.md) - Documentación detallada de APIs

## Para la presentación en clase

### Demostración recomendada

1. **Setup inicial**
   ```bash
   python main.py
   ```

2. **Casos de uso básicos**
   - `clima medellin`
   - `temperatura hoy?`
   - `va a llover?`

3. **Con zonas**
   - `clima en el poblado`
   - `hace frio en arvi?`

4. **Casos edge**
   - `clima en bogota` (rechaza)
   - `hola` (pide aclaración)

### Puntos clave para explicar

✨ **Sin frameworks**: Implementación manual de agente
✨ **Datos reales**: Open-Meteo como fuente de verdad
✨ **Respuestas naturales**: Ollama para redacción (si disponible)
✨ **Resiliencia**: Funciona sin Ollama (degradación elegante)
✨ **Contexto persistente**: Recuerda zonas en la sesión
✨ **Personalización**: Recomendaciones por barrio/zona

## Limitaciones y alcance

- ✅ Solo funciona para **Medellín** (por diseño)
- ⚠️ Ollama debe estar corriendo localmente (opcional pero recomendado)
- ⚠️ Requiere conexión a internet para Open-Meteo
- ⚠️ El pronóstico es del día actual solamente
# AgentIa_ClimaMed
