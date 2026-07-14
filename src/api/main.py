from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Importamos el motor real del chatbot desde la carpeta brain
from src.brain.chatbot_motor import ChatbotMantenimiento

app = FastAPI(
    title="API Sistema de Predicción y Procesamiento Asistido - B Mant Com 601",
    version="1.0.0"
)

# Inicializamos el chatbot globalmente al arrancar la API
bot = ChatbotMantenimiento()

# Modelos de datos para validar lo que ingresa el frontend
class ConsultaInput(BaseModel):
    pregunta: str

class SolicitudInput(BaseModel):
    unidad: str
    falla_descripcion: str


@app.get("/")
def read_root():
    """Da la bienvenida e imprime el menú inicial estructurado."""
    return {
        "status": "online",
        "mensaje_bienvenida": bot.saludar_usuario()
    }


@app.post("/consulta")
def procesar_consulta(data: ConsultaInput):
    """Flujo A: Procesa preguntas en Lenguaje Natural usando el pipeline RAG."""
    if not data.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    
    # Consumimos el método real de búsqueda en manuales
    respuesta_rag = bot.simular_flujo_consulta_rag(data.pregunta)
    
    return {
        "tipo_flujo": "A - Consulta Técnica",
        "pregunta_recibida": data.pregunta,
        "respuesta_sistema": respuesta_rag
    }


@app.post("/solicitud")
def procesar_solicitud(data: SolicitudInput):
    """Flujo B: Clasifica la falla, valida la unidad y asigna Nro de Control."""
    if not data.unidad.strip() or not data.falla_descripcion.strip():
        raise HTTPException(status_code=400, detail="La unidad y la descripción son requeridas.")
    
    # Consumimos la lógica real usando 'dato_unidad' para que coincida con el motor
    resultado_registro = bot.procesar_y_guardar_solicitud(
        dato_unidad=data.unidad,
        texto_falla=data.falla_descripcion
    )
    
    return {
        "tipo_flujo": "B - Carga de Solicitud de Mantenimiento",
        "nro_control": resultado_registro["nro_control"],
        "unidad_validada_en_db": resultado_registro["unidad_validada"],
        "detalle_procesado": resultado_registro["datos_solicitud"]
    }