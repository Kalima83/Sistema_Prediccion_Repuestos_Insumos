# Sistema_Prediccion_Repuestos_Insumos
El sistema está diseñado bajo principios de MLOps y contenedorizado con Docker para asegurar la portabilidad en el entorno Cloud del EA.

## Estructura

PROYECTO-FINAL-BAZAN/
├── data/
│   ├── raw/                # Datos históricos de fallos (Ejército Argentino)
│   ├── processed/          # Datos limpios tras fase de Preparación (CRISP-DM)
│   └── vector_db/          # Base de datos vectorial (ChromaDB) para el RAG
├── docker/
│   ├── Dockerfile          # Configuración de la imagen Python/IA
│   └── entrypoint.sh       # Script de inicio del contenedor
├── src/
│   ├── api/
│   │   └── main.py         # API FastAPI (Interfaz del ChatBot)
│   ├── brain/
│   │   ├── model.py        # Lógica de ML para clasificación de fallos
│   │   └── rag_engine.py   # Motor RAG para consulta de manuales técnicos
│   ├── utils/
│   │   └── reports.py      # Generador de reportes PDF/Excel (HU5/HU7)
│   └── database.py         # Conector a PostgreSQL/Stock
├── tests/                  # Pruebas unitarias para validar Sprints
├── .env                    # Variables de entorno (llaves de API, credenciales)
├── docker-compose.yml      # Orquestación de API + DB Vectorial
└── requirements.txt        # Librerías (LangChain, Scikit-learn, Pandas)
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
     
