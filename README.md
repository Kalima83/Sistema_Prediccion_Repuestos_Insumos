# Sistema de Predicción de Repuestos e Insumos — B Mant Com 601

Este sistema está diseñado bajo principios de arquitectura limpia, empaquetado para asegurar portabilidad en entornos locales y futuras migraciones al entorno Cloud del Ejército Argentino (EA). 

El núcleo actual del sistema resuelve de forma nativa la ingesta, validación flexible de unidades, efectos y fallas desde fuentes de datos reales (`.xlsx`), y gestiona las transacciones mediante un árbol de decisión persistido en una base de datos local.

---

## Estructura del Proyecto y Estado de Componentes

```text
PROYECTO-FINAL-BAZAN/
├── data/                                       # Capa de Persistencia de Datos
│   ├── raw/                                    # [A FUTURO] Datos históricos de fallos sin procesar
│   ├── processed/                              # [A FUTURO] Dataset limpio (Post-Fase 3 de CRISP-DM)
│   ├── vector_db/                              # [A FUTURO] Almacenamiento de embeddings para RAG
│   ├── lista de unidades.xlsx                  # [DESARROLLADO] Base de datos real de unidades militares
│   ├── Efectos_electronica_y_electricidad.xlsx # [DESARROLLADO] Catálogo real de efectos
│   ├── CODIGO_DE_FALLAS.xlsx                   # [DESARROLLADO] Catálogo estándar de fallas
│   └── sistema_mantenimiento.db                # [DESARROLLADO] Base SQLite relacional de producción
│
├── src/                                        # Código Fuente del Sistema
│   ├── backend/                                # Lógica del Servidor, IA y Reglas de Negocio
│   │   ├── api/
│   │   │   └── main.py                         # [DESARROLLADO] Endpoints en FastAPI para el ChatBot (HU1 y HU2)
│   │   ├── brain/
│   │   │   ├── chatbot_motor.py                # [DESARROLLADO] Intérprete, ruteo de estados y formato 26/XXXX
│   │   │   ├── model.py                        # [A FUTURO] Clasificador automático de fallas mediante ML
│   │   │   └── rag_engine.py                   # [A FUTURO] Pipeline de extracción (RAG) sobre manuales técnicos
│   │   ├── core/
│   │   │   ├── procesamiento_inventario.py     # [DESARROLLADO] Motor de ingesta nativa de archivos Excel
│   │   │   └── base_datos.py                   # [DESARROLLADO] Repositorio de persistencia e historial SQL
│   │   └── utils/
│   │       ├── seguridad.py                    # [A FUTURO] Cifrado criptográfico de datos sensibles
│   │       └── reports.py                      # [A FUTURO] Generador automatizado de PDF/Excel (HU5 y HU7)
│   │
│   └── frontend/                               # Interfaz Gráfica del Usuario
│       └── app.py                              # [DESARROLLADO] UI interactiva y visual desarrollada con Streamlit
│
├── .env                                        # [DESARROLLADO] Configuración de variables de entorno
├── .gitignore                                  # [DESARROLLADO] Exclusión de binarios y entornos virtuales
└── requirements.txt                            # [DESARROLLADO] Dependencias optimizadas del entorno de ejecución

## Tecnologías Proyectadas y Utilizadas

* **Gestión de Datos e Ingesta:** Python 3.10+ y Pandas (Procesamiento nativo de planillas de Arsenales e integridad referencial).
* **Persistencia Local:** SQLite3 (Motor relacional embebido para el cálculo automático de números de control e historial).
* **Motor de API:** FastAPI + Uvicorn (Arquitectura desacoplada para comunicación síncrona de alta performance).
* **Interfaz Visual:** Streamlit (Despliegue ágil de UI interactiva para operadores de mantenimiento).
* **Capa de Seguridad e Integridad:** Algoritmo de cifrado simétrico (AES-256) planificado en `src/backend/utils/seguridad.py` para la protección de la información operativa sensible y datos de mantenimiento restringidos.
* **[A FUTURO] Inteligencia Artificial & RAG:** Scikit-learn / TensorFlow para la clasificación predictiva de componentes, junto con LangChain + Vector DB (ChromaDB/Qdrant) para la explotación de manuales técnicos en Lenguaje Natural.
* **[A FUTURO] Infraestructura:** Contenedores Docker y Orquestación con Docker Compose para asegurar el despliegue homogéneo en el entorno del EA.

---

## Estado de las Funcionalidades (Historias de Usuario - HU)

### 1. Gestión de Solicitudes (Épica 1 & 2)
* **Asistente Virtual (Árbol de Decisión):** *¡DESARROLLADO!* El chatbot interactúa mediante una interfaz guiada dividida en dos flujos independientes: Flujo A (Consultas) y Flujo B (Carga de Mantenimiento) para guiar al usuario en la carga de datos en lenguaje natural.
* **Validación de Datos del Catálogo:** *¡DESARROLLADO!* El motor procesa texto libre y valida de forma automática contra los registros reales analizando Códigos, Nombres Completos o Abreviaturas (ej: "Comunicaciones Mecanizada 10"), asegurando la integridad referencial.
* **Persistencia e Identificación Operativa:** *¡DESARROLLADO!* Las solicitudes confirmadas se graban en la base de datos local y se les asigna un Identificador único correlativo institucional con el formato `26/XXXX` (Año/Número).
* **Sistema de Carga Restringida (5 Campos):** *[A DESARROLLAR A FUTURO]* Implementación del bloqueo de interfaz que exigirá la carga mandatoria de 5 campos obligatorios para asegurar un 90% de precisión técnica antes de impactar el sistema central.
* **Categorización Semántica (PLN):** *[A DESARROLLAR A FUTURO]* Motor inteligente basado en Machine Learning para diferenciar automáticamente problemas estandarizados de casos complejos o fallas atípicas.
* **Explotación del Manual de Usuario (RAG):** *[A DESARROLLAR A FUTURO]* Conexión del motor RAG (`rag_engine.py`) a la base vectorial para resolver dudas complejas en Lenguaje Natural dentro del Flujo A.
* **Resguardo Criptográfico:** *[A DESARROLLAR A FUTURO]* Ofuscación simétrica de los datos sensibles de mantenimiento mediante el módulo de seguridad.

### 2. Logística y Compras (Épica 3)
* **Predicción de Insumos Críticos:** *[A DESARROLLAR A FUTURO]* Algoritmo encargado de predecir y generar automáticamente la lista optimizada de repuestos necesarios (formato `.xlsx`) en menos de 3 minutos por solicitud procesada.
* **Control de Stock y Alertas:** *[A DESARROLLAR A FUTURO]* Módulo de monitoreo de inventario en talleres con disparadores de alertas automáticas ante stock insuficiente o niveles críticos de repuestos de electrónica.

### 3. Monitoreo y Reportes (Épica 4)
* **Dashboard de Eficiencia Operativa:** *[A DESARROLLAR A FUTURO]* Panel de control para el seguimiento en tiempo real de los tiempos de reparación, configurado con alertas visuales automáticas si el proceso supera el 10% del tiempo estimado de mano de obra.
* **Módulo de Exportación Automatizada:** *[A DESARROLLAR A FUTURO]* Lógica alojada en `src/backend/utils/