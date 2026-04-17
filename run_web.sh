#!/bin/bash

# Script para iniciar la aplicación web del Agente de Clima

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║    AGENTE DE IA PARA CLIMA - INTERFAZ WEB                   ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

# Verificar si Python está disponible
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    exit 1
fi

echo "✅ Python3 encontrado"

# Verificar si estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py no encontrado. Ejecuta esto desde el directorio del proyecto."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d ".venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv .venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source .venv/bin/activate

# Instalar/actualizar dependencias
echo "📚 Verificando dependencias..."
pip install --upgrade -r requirements.txt -q

# Iniciar la aplicación
echo ""
echo "🚀 Iniciando servidor..."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "   📊 Servidor corriendo en: http://localhost:5000"
echo "   🌐 Abre este URL en tu navegador"
echo "   📁 Para detener: Presiona Ctrl+C"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Ejecutar la aplicación
python app.py
