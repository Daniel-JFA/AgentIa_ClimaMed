@echo off
REM Script para iniciar la aplicación web en Windows

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║    AGENTE DE IA PARA CLIMA - INTERFAZ WEB                   ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está disponible
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Error: Python no está instalado
    exit /b 1
)

echo ✅ Python encontrado

REM Verificar si estamos en el directorio correcto
if not exist "app.py" (
    echo ❌ Error: app.py no encontrado
    exit /b 1
)

REM Crear entorno virtual si no existe
if not exist ".venv" (
    echo 📦 Creando entorno virtual...
    python -m venv .venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call .venv\Scripts\activate.bat

REM Instalar/actualizar dependencias
echo 📚 Verificando dependencias...
pip install --upgrade -r requirements.txt -q

REM Iniciar la aplicación
echo.
echo 🚀 Iniciando servidor...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo    📊 Servidor corriendo en: http://localhost:5000
echo    🌐 Abre este URL en tu navegador
echo    📁 Para detener: Presiona Ctrl+C
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Ejecutar la aplicación
python app.py

pause
