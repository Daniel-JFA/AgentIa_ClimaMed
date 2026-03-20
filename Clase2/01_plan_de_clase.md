# Clase 2 — Estructura completa

## Tema
**Construcción de un agente de clima real con API + Ollama**

## Duración sugerida
**2 horas**

## Resultado esperado
Al final de la clase, el estudiante debe poder:

- explicar la diferencia entre un chatbot y un agente,
- identificar qué es una tool,
- comprender el flujo `usuario → agente → API → modelo → respuesta`,
- ejecutar un agente funcional con API real y Ollama,
- modificar el agente para agregar ciudades o reglas nuevas.

## Estructura de la clase

### 1. Apertura — 10 min
- conectar con la clase anterior,
- explicar que hoy se pasa de ejemplo simulado a agente real.

### 2. Repaso conceptual — 15 min
- agente vs chatbot,
- tools,
- memoria simple,
- uso de Ollama.

### 3. Arquitectura — 15 min
Flujo:
`Usuario → Agente → API de clima → Ollama → Respuesta`

### 4. Código por módulos — 25 min
- `tools/weather_api.py`
- `agents/weather_agent_real.py`

### 5. Demo en vivo — 20 min
Pruebas:
- `¿Va a llover hoy en Medellín?`
- `Laureles`
- `¿Necesito sombrilla?`
- `¿Cómo está el clima en Bogotá?`

### 6. Trabajo guiado — 25 min
Cada estudiante debe extender una parte del agente.

### 7. Cierre — 10 min
Conclusión:
> Un agente útil combina datos reales, contexto y generación de lenguaje natural.
