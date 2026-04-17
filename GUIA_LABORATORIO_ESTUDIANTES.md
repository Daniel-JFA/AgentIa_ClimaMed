# Guia de Laboratorio - Agente de IA de Clima (Medellin)

Duracion sugerida: 45-60 minutos  
Modalidad: individual o parejas  
Entrega: capturas + respuestas breves

---

## Objetivo

Dejar el proyecto funcionando en:
1. Modo terminal (CLI)
2. Modo web (Flask)
3. Endpoint API (POST /api/ask)

Ademas, validar que la respuesta cambie segun la intencion de la pregunta (lluvia, temperatura, humedad, viento).

---

## Requisitos previos

- Python 3.10+
- Git
- Internet (para Open-Meteo)
- Ollama opcional (el proyecto funciona sin Ollama)

---

## Parte A - Instalacion

### Linux / Mac

1. Clona el repositorio

```bash
git clone URL_DEL_REPO
cd agente_clima_medellin
```

2. Crea y activa entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instala dependencias

```bash
pip install -r requirements.txt
```

### Windows (PowerShell)

1. Clona el repositorio

```powershell
git clone URL_DEL_REPO
cd agente_clima_medellin
```

2. Crea y activa entorno virtual

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

3. Instala dependencias

```powershell
pip install -r requirements.txt
```

---

## Parte B - Ejecucion

### 1) Modo terminal

```bash
python main.py
```

Prueba estas preguntas:
- clima en medellin
- temperatura en medellin
- humedad en medellin
- como esta el viento en medellin

### 2) Modo web

```bash
python app.py
```

Abre en navegador:
- http://127.0.0.1:5000

### 3) Prueba de API

En otra terminal:

```bash
curl -s -X POST http://127.0.0.1:5000/api/ask \
-H "Content-Type: application/json" \
-d '{"question":"humedad en medellin"}'
```

```bash
curl -s -X POST http://127.0.0.1:5000/api/ask \
-H "Content-Type: application/json" \
-d '{"question":"como esta el viento en medellin"}'
```

Resultado esperado: respuestas diferentes por intencion.

---

## Parte C - Checklist de validacion

Marca cada item con SI o NO:

- [SI] Se creo y activo el entorno virtual
- [SI] Se instalaron dependencias sin error
- [SI] El CLI responde en terminal
- [SI] La web abre en http://127.0.0.1:5000
- [SI] El endpoint /health responde OK
- [SI] El endpoint /api/ask responde JSON valido
- [SI] La respuesta cambia entre humedad y viento
- [SI] El agente rechaza ciudades fuera de Medellin

---

## Parte D - Evidencias de entrega

Adjunta 4 evidencias:

1. Captura de terminal con instalacion (venv + pip)
2. Captura de CLI respondiendo una pregunta
3. Captura de navegador con la interfaz web
4. Captura de dos respuestas API distintas (humedad vs viento)

---

## Parte E - Preguntas cortas (responder en 3-5 lineas)

1. Que API aporta los datos reales del clima?
2. Que pasa si Ollama no esta disponible?
3. Por que este agente no responde sobre Bogota o Cali?
4. Que ventaja tiene separar CLI, Web y API?

---

## Rúbrica simple (10 puntos)

1. Instalacion correcta (2 pts)
2. CLI funcional (2 pts)
3. Web funcional (2 pts)
4. API funcional y variacion por intencion (3 pts)
5. Respuestas cortas bien justificadas (1 pt)

---

## Solucion de problemas rapida

1. Error de modulo no encontrado
- Verifica que el entorno virtual este activo
- Reinstala: pip install -r requirements.txt

2. Puerto 5000 ocupado
- Cierra proceso anterior o cambia puerto en app.py

3. Respuesta repetida en navegador
- Haz recarga dura (Ctrl+Shift+R)
- Reinicia app.py

4. Ollama no responde
- No bloquea el laboratorio: debe funcionar fallback

---

## Extension opcional (bonus)

Implementa una mejora y muestra evidencia:
- Agregar nueva zona reconocida
- Agregar nueva palabra clave de intencion
- Mejorar un mensaje de fallback
