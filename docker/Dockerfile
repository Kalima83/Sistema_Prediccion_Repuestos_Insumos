# Usamos una imagen liviana oficial de Python
FROM python:3.10-slim

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias (por ejemplo, para compilar ciertas librerías)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalamos las librerías de Python de tu tesis
RUN pip install --no-cache-dir -r requirements.txt

# El código se monta mediante volúmenes en el docker-compose, 
# pero dejamos expuesto el puerto por defecto de la API
EXPOSE 8000

# Comando para arrancar FastAPI con Uvicorn en modo desarrollo
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]