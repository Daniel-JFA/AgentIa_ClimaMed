
Ejemplo básico de Agente de IA
Consulta de clima (ejemplo Medellín)

Estructura:

main.py
simple_agent.py
weather_tool.py

Cómo ejecutarlo:

1. Abrir terminal en la carpeta del proyecto
2. Ejecutar:

python main.py

Ejemplo de uso:

Pregunta: clima medellin
Agente: El clima en medellin es 25°C, parcialmente nublado con posibilidad de lluvia


-----------------------------------
Agente de Logistica con BD MySQL
-----------------------------------

Archivos nuevos:

main_logistics.py
logistics_agent.py
logistics_tool.py

Como ejecutarlo:

python main_logistics.py

Ejemplos de preguntas:

Pregunta: repartidor mas cercano 6.2442 -75.5812
Pregunta: costo promedio por km
Pregunta: cuanto tarda 8.4 km carga 2

Configuracion BD (opcional por variables de entorno):

LOGISTIC_DB_HOST (default 127.0.0.1)
LOGISTIC_DB_PORT (default 3306)
LOGISTIC_DB_USER (default root)
LOGISTIC_DB_PASS (default root)
LOGISTIC_DB_NAME (default Logistic)


-----------------------------------
Integracion con Ollama (main.py)
-----------------------------------

El main unificado (clima + logistica) usa Ollama para clasificar preguntas
ambiguas cuando no encuentra palabras clave directas.

Comando de chequeo dentro del chat:

estado ollama

Debe mostrar algo como:

ollama=conectado_modelo_ok

Pasos para habilitar:

1. Iniciar Ollama:
	ollama serve

2. Descargar modelo (ejemplo):
	ollama pull llama3.2:3b

3. Ejecutar agente:
	python main.py

Variables opcionales:

OLLAMA_HOST (default http://127.0.0.1:11434)
OLLAMA_MODEL (default llama3.2:3b)
