import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Importamos el motor del chatbot
from src.backend.brain.chatbot_motor import ChatbotMantenimiento

# Instanciamos el router. Le ponemos un prefijo para que las rutas queden ordenadas.
router = APIRouter(prefix="/reparacion", tags=["Flujo B - Reparaciones"])

# Inicializamos el motor
bot = ChatbotMantenimiento()

# --- MODELOS DE DATOS ---
class TraduccionInput(BaseModel):
    texto_libre: str

class SolicitudInput(BaseModel):
    unidad: str
    equipo: str
    codigo_falla: str
    descripcion_procesada: str

# --- ENDPOINTS DE LECTURA DE CATÁLOGOS (EXCEL) ---
@router.get("/unidades")
def obtener_unidades():
    """Lee el Excel real y devuelve la lista de unidades."""
    try:
        df = pd.read_excel("data/lista de unidades.xlsx")
        return df.iloc[:, 0].dropna().unique().tolist()
    except Exception as e:
        print(f"Error leyendo unidades: {e}")
        return ["Error al cargar unidades"]

@router.get("/equipos")
def obtener_equipos():
    """Lee el Excel real y devuelve la lista de efectos/equipos."""
    try:
        df = pd.read_excel("data/Efectos_electronica_y_electricidad.xlsx")
        return df.iloc[:, 0].dropna().unique().tolist()
    except Exception as e:
        print(f"Error leyendo equipos: {e}")
        return ["Error al cargar equipos"]

@router.get("/fallas")
def obtener_fallas():
    """Lee el Excel real de fallas y agrega la opción para fallas nuevas."""
    try:
        df = pd.read_excel("data/CODIGO_DE_FALLAS.xlsx")
        fallas = df.iloc[:, 0].dropna().unique().tolist()
        fallas.append("Otra (Ingresar nueva falla)")
        return fallas
    except Exception as e:
        print(f"Error leyendo fallas: {e}")
        return ["Otra (Ingresar nueva falla)"]

# --- ENDPOINTS DE PROCESAMIENTO ---
@router.post("/traducir_falla")
def traducir_falla(data: TraduccionInput):
    """
    Toma el texto libre del usuario y simula la traducción técnica 
    (Human-in-the-loop) para que el operador confirme.
    """
    if not data.texto_libre.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")
    
    # Simulación de la IA procesando el lenguaje natural
    texto_limpio = f"El operador reporta: {data.texto_libre.strip().capitalize()}. Requiere inspección técnica."
    
    return {
        "texto_original": data.texto_libre,
        "texto_traducido": texto_limpio
    }

@router.post("/solicitud")
def procesar_solicitud(data: SolicitudInput):
    """Guarda la solicitud final con todos los datos estructurados."""
    # Unimos el código estructurado con la descripción validada por el humano
    texto_final = f"[{data.codigo_falla}] Equipo: {data.equipo} - Detalle: {data.descripcion_procesada}"
    
    resultado_registro = bot.procesar_y_guardar_solicitud(
        dato_unidad=data.unidad,
        texto_falla=texto_final
    )
    
    return {
        "nro_control": resultado_registro["nro_control"],
        "resumen_carga": {
            "unidad": data.unidad,
            "equipo": data.equipo,
            "falla_estructurada": data.codigo_falla,
            "diagnostico_ia": data.descripcion_procesada
        }
    }