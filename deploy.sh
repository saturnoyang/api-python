#!/bin/bash

# Salir inmediatamente si un comando falla
set -e

# Nombre del entorno virtual
VENV_NAME="rumbita.cl"
PROJECT_DIR=$(dirname "$0") # Directorio donde se encuentra este script

echo "--- Navegando al directorio del proyecto: $PROJECT_DIR ---"
cd "$PROJECT_DIR"

echo "--- Verificando la existencia de Python 3 y pip ---"
if ! command -v python3 &> /dev/null
then
    echo "Error: python3 no está instalado. Por favor, instálalo."
    exit 1
fi

if ! command -v pip3 &> /dev/null
then
    echo "Error: pip3 no está instalado. Por favor, instálalo."
    exit 1
fi

echo "--- Creando o actualizando entorno virtual ($VENV_NAME) ---"
# Eliminar el entorno virtual si ya existe para asegurar una instalación limpia
if [ -d "$VENV_NAME" ]; then
    echo "Eliminando entorno virtual existente: $VENV_NAME"
    rm -rf "$VENV_NAME"
fi

# Crear un nuevo entorno virtual
python3 -m venv "$VENV_NAME"
echo "Entorno virtual '$VENV_NAME' creado."

echo "--- Activando entorno virtual '$VENV_NAME' ---"
# Activar el entorno virtual
source "$VENV_NAME"/bin/activate
echo "Entorno virtual '$VENV_NAME' activado."

echo "--- Instalando dependencias desde requirements.txt ---"
# Asegúrate de que tu archivo requirements.txt esté en el mismo directorio que este script
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "Dependencias instaladas exitosamente."
else
    echo "Error: No se encontró 'requirements.txt' en el directorio del proyecto."
    exit 1
fi

echo "--- Lanzando la aplicación FastAPI con Uvicorn ---"
# Para desarrollo, se puede usar --reload.
# Para producción, se recomienda usar un gestor de procesos (como Gunicorn)
# y NO usar --reload.
uvicorn main:app --host 0.0.0.0 --port 8000