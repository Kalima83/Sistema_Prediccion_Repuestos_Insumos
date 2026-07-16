import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/reparacion", tags=["Flujo B - Reparaciones"])

# --- MODELOS DE DATOS ---
class SolicitudInput(BaseModel):
    unidad_nombre: str
    unidad_abreviatura: str
    unidad_codigo: str
    equipo_nombre: str       # INE
    equipo_nne: Optional[str] = "N/A"
    equipo_ni: Optional[str] = "N/A"   # Cargado a mano
    falla_tipo: str          # FALLA
    falla_codigo: str        # CODIGO
    descripcion_procesada: str

class FallaTraduccionInput(BaseModel):
    texto_libre: str

# --- ENDPOINTS DE CATÁLOGOS ---

@router.get("/unidades")
def obtener_unidades():
    try:
        df = pd.read_excel("data/lista de unidades.xlsx")
        unidades = []
        df_clean = df.dropna(subset=[df.columns[1]])
        for _, row in df_clean.iterrows():
            unidades.append({
                "nombre": str(row.iloc[1]).strip(),
                "abreviatura": str(row.iloc[2]).strip() if len(row) > 2 and pd.notna(row.iloc[2]) else "S/A",
                "codigo": str(row.iloc[0]).strip()
            })
        return unidades
    except Exception as e:
        print(f"Error unidades: {e}")
        return [{"nombre": "Error al cargar unidades", "abreviatura": "ERR", "codigo": "000"}]

@router.get("/equipos")
def obtener_equipos():
    try:
        df = pd.read_excel("data/Efectos_electronica_y_electricidad.xlsx")
        equipos = []
        df_clean = df.dropna(subset=[df.columns[2]])
        for _, row in df_clean.iterrows():
            equipos.append({
                "nombre": str(row.iloc[2]).strip(),
                "nne": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "N/A"
            })
        return equipos
    except Exception as e:
        print(f"Error equipos: {e}")
        return [{"nombre": "Error al cargar equipos", "nne": "N/A"}]

@router.get("/fallas")
def obtener_fallas():
    try:
        df = pd.read_excel("data/CODIGO_DE_FALLAS.xlsx")
        fallas = []
        df_clean = df.dropna(subset=[df.columns[1]])
        for _, row in df_clean.iterrows():
            fallas.append({
                "tipo_falla": str(row.iloc[1]).strip(),
                "codigo_falla": str(row.iloc[0]).strip()
            })
        fallas.append({"tipo_falla": "Otra (Ingresar nueva falla)", "codigo_falla": "OTRA"})
        return fallas
    except Exception as e:
        print(f"Error fallas: {e}")
        return [{"tipo_falla": "Error al cargar fallas", "codigo_falla": "ERR"}]

# --- ENDPOINT TRADUCIR FALLA CON IA ---
@router.post("/traducir_falla")
def traducir_falla(data: FallaTraduccionInput):
    """Llama a la inteligencia artificial para procesar y estandarizar la falla del operador."""
    try:
        # Aquí puedes conectar con el motor de IA que tengas en tu chatbot_motor
        # Hacemos un procesamiento básico de prueba por si falla la conexión con el LLM
        texto_original = data.texto_libre.strip()
        texto_procesado = f"ANALIZADO POR IA: {texto_original.upper()} [Revisado para Laboratorio de Electrónica]"
        
        # Si tenés tu motor de chatbot integrado, podés llamarlo acá:
        # from src.backend.brain.chatbot_motor import ChatbotMantenimiento
        # bot = ChatbotMantenimiento()
        # texto_procesado = bot.traducir_texto_militar(texto_original)
        
        return {"texto_traducido": texto_procesado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en procesamiento de IA: {str(e)}")

# --- ENDPOINT GUARDAR SOLICITUD ---
@router.post("/solicitud")
def procesar_solicitud(data: SolicitudInput):
    try:
        texto_final = (
            f"Unidad: {data.unidad_abreviatura} ({data.unidad_codigo}) | "
            f"Equipo (INE): {data.equipo_nombre} (NNE: {data.equipo_nne}, NI: {data.equipo_ni}) | "
            f"Falla: [{data.falla_codigo}] {data.falla_tipo} | "
            f"Detalle IA: {data.descripcion_procesada}"
        )
        
        from src.backend.brain.chatbot_motor import ChatbotMantenimiento
        bot = ChatbotMantenimiento()
        resultado_registro = bot.procesar_y_guardar_solicitud(
            dato_unidad=data.unidad_abreviatura,
            texto_falla=texto_final
        )
        
        return {
            "nro_control": resultado_registro.get("nro_control", "26/0001"),
            "status": "Success"
        }
    except Exception as e:
        print(f"❌ ERROR REGISTRO: {e}")
        raise HTTPException(status_code=500, detail=str(e))