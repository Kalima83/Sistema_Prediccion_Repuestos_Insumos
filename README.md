# Sistema_Prediccion_Repuestos_Insumos
El sistema está diseñado bajo principios de MLOps y contenedorizado con Docker para asegurar la portabilidad en el entorno Cloud del EA.

## Estructura
.
├── .github/workflows/       # CI/CD para MLOps
├── data/                    # Datos históricos y bases vectoriales
├── docker/                  # Dockerfile y configuración de contenedores
├── docs/                    # Memoria técnica y manuales de usuario 
├── src/                     # Código fuente principal
│   ├── api/                 # API ChatBot (FastAPI/Flask)
│   ├── brain/               # Lógica de ML y motor RAG 
│   ├── database/            # Conexión a DB Vectorial y SQL (Stock/Equipos)
│   └── reports/             # Generador de informes PDF/XLSX 
├── tests/                   # Pruebas unitarias e integración 
├── docker-compose.yml       # Orquestación de servicios
└── requirements.txt         # Dependencias de Python

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
     
