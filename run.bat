@echo off
REM Script para ejecutar la API de FastAPI en Windows

REM Navegar al directorio donde se encuentra este script
cd /d "%~dp0"

echo --- Activando entorno virtual ---
REM Activar el entorno virtual
REM Si rumbita_api está DENTRO de api-python, usar la ruta directa
call .\rumbita_api\Scripts\activate 

echo --- Lanzando la aplicación FastAPI con Uvicorn ---
REM Iniciar Uvicorn con recarga automática para desarrollo
REM Usar la ruta completa al ejecutable de uvicorn dentro del entorno virtual
REM Si rumbita_api está DENTRO de api-python, usar la ruta directa
.\rumbita_api\Scripts\uvicorn main:app --reload 

REM Pausa opcional para ver mensajes antes de que la ventana se cierre si Uvicorn termina
REM pause