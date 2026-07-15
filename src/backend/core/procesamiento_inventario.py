import os
import pandas as pd
from typing import Dict, List

# Rutas exactas a tus archivos de Excel (.xlsx) dentro de la carpeta data/
EXCEL_UNIDADES = os.path.join("data", "lista de unidades.xlsx")
EXCEL_EFECTOS = os.path.join("data", "Efectos_electronica_y_electricidad.xlsx")
EXCEL_FALLAS = os.path.join("data", "CODIGO_DE_FALLAS.xlsx")

def cargar_unidades() -> List[Dict]:
    """Carga las unidades militares desde lista de unidades.xlsx"""
    if not os.path.exists(EXCEL_UNIDADES):
        print(f"Alerta: No se encontro el archivo {EXCEL_UNIDADES}")
        return []
    try:
        # Se lee la Hoja1 y especificamos el motor openpyxl para asegurar compatibilidad
        df = pd.read_excel(EXCEL_UNIDADES, sheet_name="Hoja1", engine="openpyxl")
        df.columns = df.columns.str.strip()
        
        resultado = []
        for _, fila in df.iterrows():
            unidad = str(fila.get("Unidad", "")).strip()
            if unidad == "" or unidad.lower() == "nan":
                continue
            resultado.append({
                "codigo_u": unidad,
                "nombre_unidad": str(fila.get("Descripcion", "")).strip(),
                "primer_nivel_comando": str(fila.get("1er N Dep", "No especificado")).strip()
            })
        return resultado
    except Exception as e:
        print(f"Error en Unidades (Excel): {str(e)}")
        return []

def procesar_efectos() -> List[Dict]:
    """Carga los efectos desde Efectos_electronica_y_electricidad.xlsx"""
    if not os.path.exists(EXCEL_EFECTOS):
        print(f"Alerta: No se encontro el archivo {EXCEL_EFECTOS}")
        return []
    try:
        df = pd.read_excel(EXCEL_EFECTOS, sheet_name="Hoja1", engine="openpyxl")
        df.columns = df.columns.str.strip()
        
        resultado = []
        for _, fila in df.iterrows():
            nro_ord = str(fila.get("N° Ord", "")).strip()
            if nro_ord == "" or nro_ord.lower() == "nan":
                continue
                
            nne = str(fila.get("NNE", "")).strip()
            ine = str(fila.get("INE", "")).strip()
            
            if nne == "" or nne.lower() in ["nan", "sin catalogar", "s/c", "0"]:
                catalogado = False
                nne_final = "SIN CATALOGAR"
                ine_final = ine if ine and ine.lower() != "nan" else "REQUERIDO_MANUAL"
            else:
                catalogado = True
                nne_final = nne
                ine_final = ine

            resultado.append({
                "nro_orden": nro_ord,
                "nne": nne_final,
                "ine": ine_final,
                "catalogado": catalogado
            })
        return resultado
    except Exception as e:
        print(f"Error en Efectos (Excel): {str(e)}")
        return []

def cargar_fallas_estandarizadas() -> List[Dict]:
    """Carga el catalogo de fallas desde CODIGO_DE_FALLAS.xlsx"""
    if not os.path.exists(EXCEL_FALLAS):
        print(f"Alerta: No se encontro el archivo {EXCEL_FALLAS}")
        return []
    try:
        df = pd.read_excel(EXCEL_FALLAS, sheet_name="Hoja1", engine="openpyxl")
        df.columns = df.columns.str.strip()
        
        resultado = []
        for _, fila in df.iterrows():
            codigo = str(fila.get("CODIGO", "")).strip()
            if codigo == "" or codigo.lower() == "nan":
                continue
                
            resultado.append({
                "codigo_falla": codigo.zfill(3),
                "falla_estandar": str(fila.get("FALLA", "")).strip(),
                "referencia_sintomas": str(fila.get("REFERENCIA", "")).strip()
            })
        return resultado
    except Exception as e:
        print(f"Error en Fallas (Excel): {str(e)}")
        return []

if __name__ == "__main__":
    print("Iniciando procesamiento de archivos Excel reales...")
    unidades = cargar_unidades()
    efectos = procesar_efectos()
    fallas = cargar_fallas_estandarizadas()
    
    print("\n=========================================")
    print("      REPORTE DE INGESTA DE DATOS       ")
    print("=========================================")
    print(f"Unidades Militares:          {len(unidades)} registros.")
    print(f"Diccionario de Efectos:      {len(efectos)} registros.")
    print(f"Catalogo Estandar de Fallas: {len(fallas)} registros.")
    print("=========================================\n")