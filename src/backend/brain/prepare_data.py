# src/brain/prepare_data.py
import re
import os
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

# ==========================================
# 1. FUNCIONES DE LIMPIEZA Y NORMALIZACIÓN
# ==========================================

def normalizar_texto_basico(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica transformaciones de texto iniciales sobre las columnas."""
    df = df.copy()
    for col in ['INE', 'PRINCIPALES FALLAS']:
        if col in df.columns:
            df[col] = df[col].astype(str).str.upper().str.strip()
            # Reemplaza múltiples espacios por uno solo
            df[col] = df[col].apply(lambda x: re.sub(r'\s+', ' ', x))
    return df

def remover_ruido_institucional(df: pd.DataFrame) -> pd.DataFrame:
    """Elimina códigos de Órdenes de Mantenimiento y firmas repetitivas."""
    df = df.copy()
    if 'PRINCIPALES FALLAS' in df.columns:
        # Remueve patrones como 'OM NRO XXXXXXX', 'FECHA XX/XX/XX', 'ESC COM BL 1', etc.
        patrones_ruido = [
            r'OM\s+NRO\s+\d+', 
            r'FECHA\s+\d{2}/\d{2}/\d{2}', 
            r'SRE\s+\d+\s+NRO\s+[\d/]+',
            r'\s*\(ESC\s+[A-Z\s\d]+\)', 
            r'\s*\(GAA\s+\d+\)',
            r'\s*\(G\s+MANT\s+[A-Z\s]+\)'
        ]
        for patron in patrones_ruido:
            df['PRINCIPALES FALLAS'] = df['PRINCIPALES FALLAS'].apply(
                lambda x: re.sub(patron, '', x, flags=re.IGNORECASE).strip()
            )
    return df

# ==========================================
# 2. DICCIONARIO Y CLASIFICACIÓN (GROUND TRUTH)
# ==========================================

DICCIONARIO_CATEGORIAS = {
    'RF': ['RADIO', 'DGP', 'DGM', 'CNR', 'SINTONIZA', 'ANTENA', 'TX', 'RX', 'BLU', 'VHF', 'HF'],
    'TELEFONIA': ['TELEFONO', 'CONMUTADOR', 'CABLE TEF', 'TA 1', 'TA 312', 'SB 22A', 'TP 9', 'CAMP'],
    'INFORMATICA': ['INFORMATICA', 'WIN10', 'COMPUTADORA', 'UPS', 'HARDWARE', 'SOFWARE', 'MONITOR', 'PC']
}

def asignar_familia_logistica(df: pd.DataFrame) -> pd.DataFrame:
    """Asigna de forma determinista la familia tecnológica basándose en palabras clave."""
    df = df.copy()
    familias = []
    
    for _, fila in df.iterrows():
        texto_falla = str(fila.get('PRINCIPALES FALLAS', ''))
        texto_ine = str(fila.get('INE', ''))
        texto_combinado = f"{texto_ine} {texto_falla}"
        
        asignado = False
        for familia, palabras in DICCIONARIO_CATEGORIAS.items():
            if any(palabra in texto_combinado for palabra in palabras):
                if familia == 'RF':
                    familias.append('Radiofrecuencia (RF)')
                elif familia == 'TELEFONIA':
                    familias.append('Telefonía y Campamento')
                elif familia == 'INFORMATICA':
                    familias.append('Informática')
                asignado = True
                break
                
        if not asignado:
            familias.append('Comunicaciones Generales')
            
    df['Familia_Real'] = familias
    return df

# ==========================================
# 3. ENSAMBLAJE DEL PIPELINE (SCIKIT-LEARN)
# ==========================================

pipeline_ingesta = Pipeline([
    ('normalizacion', FunctionTransformer(normalizar_texto_basico, validate=False)),
    ('limpieza_ruido', FunctionTransformer(remover_ruido_institucional, validate=False)),
    ('clasificacion', FunctionTransformer(asignar_familia_logistica, validate=False))
])

# ==========================================
# 4. EJECUCIÓN CON CONFIGURACIÓN DE RUTAS
# ==========================================

if __name__ == "__main__":
    # Ajustamos las rutas de acuerdo a la estructura de tu repositorio
    archivo_entrada = "data/raw/fallas_br_1.xlsx"
    archivo_salida = "data/processed/dataset_evaluacion_cap4.xlsx"
    
    if os.path.exists(archivo_entrada):
        print(f"[*] Cargando archivo original desde: {archivo_entrada}")
        df_crudo = pd.read_excel(archivo_entrada)
        
        print("[*] Ejecutando Pipeline de Adquisición y Normalización...")
        df_procesado = pipeline_ingesta.fit_transform(df_crudo)
        
        # Crear la carpeta processed si no existe
        os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
        
        print(f"[*] Guardando Dataset Procesado en: {archivo_salida}")
        df_procesado.to_excel(archivo_salida, index=False)
        print("[+] Fase de preparación de datos completada con éxito.")
    else:
        print(f"[-] Error: No se encontró el archivo en {archivo_entrada}.")