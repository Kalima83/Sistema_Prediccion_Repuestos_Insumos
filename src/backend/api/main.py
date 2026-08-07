import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos los routers modularizados
from src.backend.api.routers import reparacion_BE, consulta_BE

# Garantizamos la creación de la carpeta de almacenamiento persistente
os.makedirs("data", exist_ok=True)

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API Sistema de Predicción y Procesamiento Asistido - B Mant Com 601",
    description="Backend modularizado para gestión de mantenimiento y consultas técnicas.",
    version="2.0.0"
)

# Configuración de CORS para permitir conexiones desde el frontend de Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones desde cualquier origen local
    allow_credentials=True,
    allow_methods=["*"],  # Permite GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],
)

# Inclusión de los routers del sistema
app.include_router(consulta_BE.router)
app.include_router(reparacion_BE.router)


@app.get("/", tags=["Sistema"])
def read_root():
    """Endpoint de estado para verificar la operatividad del servidor."""
    return {
        "status": "online",
        "mensaje": "API del Sistema Logístico 601 operativa y modularizada. Lista para recibir peticiones."
    }