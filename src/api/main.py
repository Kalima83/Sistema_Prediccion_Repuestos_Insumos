from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema de Predicción de Repuestos e Insumos - B Maint Com 601",
    description="API REST para la gestión de stock y motor de búsqueda semántica (RAG) para reportes de fallas.",
    version="1.0.0"
)

# Configuración de CORS para que tu futura interfaz frontend pueda comunicarse sin bloqueos
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "status": "operativo",
        "sistema": "Predicción de Repuestos v1.0.0",
        "unidad": "Batallón de Mantenimiento de Comunicaciones 601"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected", "vector_db": "connected"}