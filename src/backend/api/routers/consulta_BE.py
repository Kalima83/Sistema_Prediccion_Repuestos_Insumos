from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Importamos el motor del chatbot
from src.backend.brain.chatbot_motor import ChatbotMantenimiento

# Instanciamos el router para el Flujo A
router = APIRouter(prefix="/consulta", tags=["Flujo A - Consultas RAG"])

# Inicializamos el motor
bot = ChatbotMantenimiento()

# --- MODELO DE DATOS ---
class ConsultaInput(BaseModel):
    pregunta: str

# --- ENDPOINT DE CONSULTA ---
@router.post("/")
def procesar_consulta(data: ConsultaInput):
    """
    Flujo A: Recibe preguntas en Lenguaje Natural y devuelve 
    respuestas basadas en los manuales técnicos (RAG).
    """
    if not data.pregunta.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía.")
    
    # Consumimos el método de búsqueda en manuales
    respuesta_rag = bot.simular_flujo_consulta_rag(data.pregunta)
    
    return {
        "pregunta_recibida": data.pregunta,
        "respuesta_sistema": respuesta_rag
    }