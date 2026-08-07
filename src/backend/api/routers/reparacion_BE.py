import os
import pickle
import pandas as pd
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

from src.backend.core.nro_control_db import (
    obtener_y_incrementar_nro_control,
    registrar_nro_control_indice,
    actualizar_asignacion_y_estado,
    listar_indice_tickets,
    consultar_nro_control
)

router = APIRouter(prefix="/reparacion", tags=["Flujo B - Reparaciones"])

# --- RUTAS ABSOLUTAS DEL PROYECTO ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
TICKETS_DIR = DATA_DIR / "tickets"


# --- MODELOS DE DATOS ---
class SolicitudInput(BaseModel):
    unidad_nombre: str
    unidad_abreviatura: str
    unidad_codigo: str
    equipo_nombre: str
    equipo_nne: Optional[str] = "N/A"
    equipo_ni: Optional[str] = "N/A"
    falla_tipo: str
    falla_codigo: str
    descripcion_procesada: str

class FallaTraduccionInput(BaseModel):
    texto_libre: str

class AsignacionInput(BaseModel):
    nro_control: str
    estado: str
    taller_asignado: str
    operador_asignado: str
    dictamen: Optional[str] = ""


# --- ENDPOINTS DE CATÁLOGOS (EXCEL) ---

@router.get("/unidades")
def obtener_unidades():
    file_path = DATA_DIR / "lista de unidades.xlsx"
    if not file_path.exists():
        print(f"⚠️ Archivo no encontrado en: {file_path}")
        return [{"nombre": "Sin datos de unidades", "abreviatura": "S/A", "codigo": "000"}]

    try:
        df = pd.read_excel(file_path)
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
        print(f"❌ Error leyendo unidades: {e}")
        return [{"nombre": "Error al cargar unidades", "abreviatura": "ERR", "codigo": "000"}]


@router.get("/equipos")
def obtener_equipos():
    file_path = DATA_DIR / "Efectos_electronica_y_electricidad.xlsx"
    if not file_path.exists():
        print(f"⚠️ Archivo no encontrado en: {file_path}")
        return [{"nombre": "Sin datos de equipos", "nne": "N/A"}]

    try:
        df = pd.read_excel(file_path)
        equipos = []
        df_clean = df.dropna(subset=[df.columns[2]])
        for _, row in df_clean.iterrows():
            equipos.append({
                "nombre": str(row.iloc[2]).strip(),
                "nne": str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else "N/A"
            })
        return equipos
    except Exception as e:
        print(f"❌ Error leyendo equipos: {e}")
        return [{"nombre": "Error al cargar equipos", "nne": "N/A"}]


@router.get("/fallas")
def obtener_fallas():
    file_path = DATA_DIR / "CODIGO_DE_FALLAS.xlsx"
    if not file_path.exists():
        print(f"⚠️ Archivo no encontrado en: {file_path}")
        return [{"tipo_falla": "Sin datos de fallas", "codigo_falla": "ERR"}]

    try:
        df = pd.read_excel(file_path)
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
        print(f"❌ Error leyendo fallas: {e}")
        return [{"tipo_falla": "Error al cargar fallas", "codigo_falla": "ERR"}]


# --- ENDPOINT IA ---

@router.post("/traducir_falla")
def traducir_falla(data: FallaTraduccionInput):
    try:
        texto_original = data.texto_libre.strip()
        texto_procesado = f"ANALIZADO POR IA: {texto_original.upper()} [Sugerido para Taller de Electrónica]"
        return {"texto_traducido": texto_procesado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en IA: {str(e)}")


# --- ENDPOINTS DE GESTIÓN DE SOLICITUDES ---

@router.post("/solicitud")
def procesar_solicitud(data: SolicitudInput):
    try:
        TICKETS_DIR.mkdir(parents=True, exist_ok=True)
        nro_control_oficial = obtener_y_incrementar_nro_control(prefijo="26")
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ruta_ticket = str(TICKETS_DIR / f"{nro_control_oficial.replace('/', '_')}.dat")
        
        datos_ticket = {
            "nro_control": nro_control_oficial,
            "unidad_nombre": data.unidad_nombre,
            "unidad_abreviatura": data.unidad_abreviatura,
            "unidad_codigo": data.unidad_codigo,
            "equipo_nombre": data.equipo_nombre,
            "equipo_nne": data.equipo_nne,
            "equipo_ni": data.equipo_ni,
            "falla_tipo": data.falla_tipo,
            "falla_codigo": data.falla_codigo,
            "descripcion_procesada": data.descripcion_procesada,
            "fecha_creacion": fecha_actual,
            "dictamen": ""
        }

        # 1. Guardar ticket pesado en disco (.dat)
        with open(ruta_ticket, "wb") as f:
            pickle.dump(datos_ticket, f)

        # 2. Guardar en el Índice SQLite
        registrar_nro_control_indice(
            nro_control=nro_control_oficial,
            ruta_ticket=ruta_ticket,
            unidad_nombre=data.unidad_nombre,
            equipo_nombre=data.equipo_nombre,
            falla_codigo=data.falla_codigo
        )

        return {"nro_control": nro_control_oficial, "status": "Success"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando solicitud: {str(e)}")


@router.get("/solicitudes")
def listar_solicitudes(operador: Optional[str] = None):
    """Retorna la lista de tickets almacenados en el índice SQLite."""
    return listar_indice_tickets(filtro_operador=operador)


@router.put("/solicitud/asignar")
def asignar_operador_y_estado(data: AsignacionInput):
    """Permite al supervisor asignar operario, taller y actualizar el dictamen del ticket."""
    try:
        actualizar_asignacion_y_estado(
            nro_control=data.nro_control,
            estado=data.estado,
            taller_asignado=data.taller_asignado,
            operador_asignado=data.operador_asignado
        )
        
        # Sincronizar el dictamen dentro del archivo .dat
        res = consultar_nro_control(data.nro_control)
        if res["existe"]:
            datos = res["datos"]
            datos["dictamen"] = data.dictamen
            ruta = datos["ruta_ticket"]
            with open(ruta, "wb") as f:
                pickle.dump(datos, f)

        return {"status": "Success", "mensaje": f"Ticket {data.nro_control} actualizado correctamente."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error actualizando asignación: {str(e)}")