# src/brain/rag_engine.py
import os
import requests
import pandas as pd
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# Configurations for local docker containers
QDRANT_URL = "http://localhost:6333"
OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "all-minilm" # O el modelo que tengas corriendo localmente
COLLECTION_NAME = "fallas_ejercito"

def obtener_embedding_local(texto: str) -> list:
    """Solicita el vector embebido al contenedor de Ollama de forma local."""
    try:
        response = requests.post(
            QDRANT_URL.replace("6333", "11434") + "/api/embeddings", # Ajuste dinámico de puerto
            json={"model": EMBEDDING_MODEL, "prompt": texto},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("embedding")
        else:
            raise Exception(f"Error en Ollama API: {response.text}")
    except Exception as e:
        print(f"[-] Error de conexión con Ollama: {e}")
        return []

def indexar_datos_en_qdrant(path_procesado: str):
    """Crea la colección y sube los vectores con metadatos a Qdrant."""
    if not os.path.exists(path_procesado):
        print(f"[-] Archivo no encontrado en: {path_procesado}. Corra primero prepare_data.py")
        return

    df = pd.read_excel(path_procesado)
    
    # Iniciar cliente de Qdrant apuntando al contenedor local
    client = QdrantClient(url=QDRANT_URL)
    
    # 1. Obtener una dimensión de prueba para configurar la colección
    print("[*] Verificando modelo de embeddings en Ollama...")
    vector_prueba = obtener_embedding_local("Prueba de dimension")
    if not vector_prueba:
        print("[-] Abortando: Asegúrese de que Ollama esté corriendo y tenga el modelo descargado.")
        return
    
    dimension = len(vector_prueba)
    print(f"[+] Conexión exitosa. Dimensión del vector del modelo '{EMBEDDING_MODEL}': {dimension}")

    # 2. Recrear la colección limpia en la base vectorial
    print(f"[*] Configurando colección '{COLLECTION_NAME}' en Qdrant...")
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dimension, distance=Distance.COSINE),
    )

    # 3. Procesar e inyectar registros en lote (Batch Ingestion)
    points = []
    print(f"[*] Vectorizando e indexando {len(df)} registros logísticos...")
    
    for idx, fila in df.iterrows():
        texto_falla = str(fila.get('PRINCIPALES FALLAS', ''))
        texto_ine = str(fila.get('INE', ''))
        
        # Combinamos el contexto para enriquecer la semántica
        contexto_combinado = f"Equipo: {texto_ine}. Falla: {texto_falla}"
        
        vector = obtener_embedding_local(contexto_combinado)
        if not vector:
            continue
            
        # Armamos la estructura del punto vectorial con su payload
        punto = PointStruct(
            id=idx,
            vector=vector,
            payload={
                "ine": texto_ine,
                "falla_original": texto_falla,
                "familia_real": str(fila.get('Familia_Real', 'Comunicaciones Generales'))
            }
        )
        points.append(punto)
        
        if (idx + 1) % 50 == 0:
            print(f"    -> Procesados {idx + 1} registros...")

    # Subida masiva a Qdrant
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"[+] Éxito: {len(points)} puntos vectoriales indexados de forma local.")

if __name__ == "__main__":
    path_data = "data/processed/dataset_evaluacion_cap4.xlsx"
    indexar_datos_en_qdrant(path_data)