# 1. Usar una imagen base de Python oficial
FROM python:3.12.1-slim

# 2. Crear un grupo y un usuario con un UID y GID específicos para mayor seguridad
RUN groupadd -r -g 1000 rumbita && useradd -r -g rumbita -u 1000 rumbita

# 3. Configurar el directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Cambiar el propietario del directorio de trabajo al usuario rumbita
RUN chown -R rumbita:rumbita /app

# 5. Copiar los archivos de requerimientos e instalarlos
# Esto ayuda a aprovechar el cache de Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar el resto del código de la aplicación
COPY . .

# 7. Cambiar al usuario rumbita. Los comandos siguientes se ejecutarán con este usuario
USER rumbita

# 8. Exponer el puerto que usará la aplicación
EXPOSE 8000

# 9. Definir el comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]