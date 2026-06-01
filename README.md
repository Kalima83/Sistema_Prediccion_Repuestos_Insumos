# Sistema_Prediccion_Repuestos_Insumos
El sistema está diseñado bajo principios de MLOps y contenedorizado con Docker para asegurar la portabilidad en el entorno Cloud del EA.

## Estructura
```text
PROYECTO-FINAL-BAZAN/
├── data/
│   ├── raw/                # Datos históricos de fallos (Ejército Argentino)
│   ├── processed/          # Datos limpios (Post-Fase 3 de CRISP-DM)
│   └── vector_db/          # Almacenamiento de embeddings para RAG
├── docker/
│   ├── Dockerfile          # Imagen base Python e instalación de dependencias
│   └── entrypoint.sh       # Script de arranque del contenedor
├── src/
│   ├── api/
│   │   └── main.py         # Interfaz del ChatBot (HU1 y HU2)
│   ├── brain/
│   │   ├── model.py        # Clasificador de fallas (ML)
│   │   └── rag_engine.py   # Motor de consulta de manuales técnicos
│   ├── utils/
│   │   └── reports.py      # Generador de PDF/Excel (HU5 y HU7)
│   └── database.py         # Gestión de stock y persistencia
├── .env                    # Variables de entorno y secretos
├── docker-compose.yml      # Orquestación de servicios
└── requirements.txt        # Librerías: LangChain, Scikit-learn, FastAPI

## Tecnologías Utilizadas

  * Lenguaje: Python 3.10+IA/ML: Scikit-learn / TensorFlow (Clasificación de fallas).
  * RAG: LangChain / LlamaIndex + Vector DB (ChromaDB/Qdrant).
  * API: FastAPI (para respuestas menores a 5 segundos).
  * Despliegue: Docker & Docker Compose.
## Funcionalidades Implementadas(HU)
  1. Gestión de Solicitudes (Épica 1 & 2)
      * Asistente Virtual: ChatBot que guía la carga de datos en lenguaje natural.
      * Categorización: Motor que diferencia problemas estandarizados de casos complejos.
      * Validación: Sistema de carga con 5 campos obligatorios para asegurar un 90% de precisión técnica.
  2. Logística y Compras (Épica 3)
       * Predicción de Insumos: Generación automática de listas de repuestos (XLSX) en menos de 3 minutos.
       * Control de Stock: Módulo de monitoreo con alertas automáticas ante stock insuficiente.
  3. Monitoreo y Reportes (Épica 4)
       * Dashboard de Eficiencia: Seguimiento de tiempos de reparación con alertas visuales si se supera el 10% del tiempo estimado.
       * Exportación: Generación de informes mensuales/semestrales en PDF y Excel.
     
