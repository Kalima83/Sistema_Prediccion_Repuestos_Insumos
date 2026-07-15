from fastapi import FastAPI
import os

# Importamos nuestros routers (módulos separados)
from src.backend.api.routers import reparacion_BE, consulta_BE

# Creamos la carpeta data de forma segura si no existe
os.makedirs("data", exist_ok=True)

# Inicializamos la aplicación FastAPI
app = FastAPI(
    title="API Sistema de Predicción y Procesamiento Asistido - B Mant Com 601",
    description="Backend modularizado para gestión de mantenimiento y consultas técnicas.",
    version="2.0.0" # Subimos la versión para celebrar la nueva arquitectura
)

# Conectamos los módulos a la aplicación principal
app.include_router(consulta_BE.router)
app.include_router(reparacion_BE.router)

@app.get("/", tags=["Sistema"])
def read_root():
    """Da la bienvenida y verifica que el servidor está online."""
    return {
        "status": "online",
        "mensaje": "API del Sistema Logístico 601 operativa y modularizada. Lista para recibir peticiones."
    }