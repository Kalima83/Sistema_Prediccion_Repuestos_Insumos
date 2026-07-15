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
│   │   │   ├── routers/                        # [NUEVO] Separación de endpoints por flujos
│   │   │   │   ├── consulta_BE.py              # [NUEVO] Endpoints del Flujo A (Consultas RAG)
│   │   │   │   └── reparacion_BE.py            # [NUEVO] Endpoints del Flujo B (Listas de Excel, Traductor y Carga)
│   │   │   └── main.py                         # [ACTUALIZADO] Orquestador principal de FastAPI que une los routers
│   │   ├── brain/
│   │   │   ├── chatbot_motor.py                # [DESARROLLADO] Intérprete, ruteo de estados y formato 26/XXXX
│   │   │   ├── prepare_data.py                 # [DESARROLLADO] Ingesta, chunking y vectorización de manuales
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
│       ├── views/                              # [NUEVO] Separación de vistas para escalabilidad
│       │   ├── consulta_FE.py                  # [NUEVO] UI del Flujo A (Chatbot de consultas técnicas)
│       │   └── reparacion_FE.py                # [NUEVO] UI del Flujo B (Carga asistida de mantenimiento)
│       └── app.py                              # [ACTUALIZADO] Orquestador visual principal (Menú lateral de Streamlit)
│
├── .env                                        # [DESARROLLADO] Configuración de variables de entorno
├── .gitignore                                  # [DESARROLLADO] Exclusión de binarios y entornos virtuales
└── requirements.txt                            # [DESARROLLADO] Dependencias optimizadas del entorno de ejecución


## Tecnologías Proyectadas y Utilizadas
* **Gestión de Datos e Ingesta:** Python 3.10+, Pandas y OpenPyXL (Lectura y procesamiento dinámico y en tiempo real de planillas de Arsenales para garantizar integridad referencial).
* **Persistencia Local:** SQLite3 (Motor relacional embebido para el cálculo automático de números de control e historial).
* **Motor de API:** FastAPI + Uvicorn (Arquitectura modular mediante `APIRouter` para comunicación síncrona de alta performance y separación de flujos).
* **Interfaz Visual:** Streamlit (Despliegue ágil de UI interactiva con menús de navegación lateral y componentes dinámicos para operadores).
* **Capa de Seguridad e Integridad:** Algoritmo de cifrado simétrico (AES-256) planificado en `src/backend/utils/seguridad.py` para la protección de la información operativa sensible y datos de mantenimiento restringidos.
* **Inteligencia Artificial, PLN & RAG:** Enfoque "Human-in-the-loop" para traducción técnica de fallas. *[A FUTURO]* Scikit-learn / TensorFlow para clasificación predictiva, y LangChain + Vector DB para explotación de manuales técnicos.
* **[A FUTURO] Infraestructura:** Contenedores Docker y Orquestación con Docker Compose para asegurar el despliegue homogéneo en el entorno del EA.

---

## Estado de las Funciones (Historias de Usuario - HU)

### 1. Gestión de Solicitudes (Épica 1 & 2)
* **Asistente Virtual (Diseño Híbrido):** *¡DESARROLLADO!* El sistema interactúa mediante una interfaz guiada y modularizada en dos flujos: Flujo A (Consultas Técnicas) y Flujo B (Carga Asistida de Mantenimiento), combinando selección estricta de datos con campos de lenguaje natural.
* **Validación de Datos Dinámica:** *¡DESARROLLADO!* La interfaz consume los catálogos en tiempo real desde el Backend (Unidades, Equipos, Códigos). Asegura 100% de precisión técnica mediante menús desplegables (`selectbox`), eliminando el error de tipeo.
* **Captura de Fallas Nuevas (Cuarentena):** *¡DESARROLLADO!* El catálogo de fallas incluye la capacidad de detectar problemas atípicos permitiendo ingresar "Nuevas Fallas" para engrosar y normalizar la base de datos a futuro.
* **Traducción Asistida (Human-in-the-loop):** *¡DESARROLLADO!* El sistema toma la novedad escrita en texto libre por el operador, la procesa mediante NLP y le devuelve una descripción técnica normalizada para su validación manual antes del guardado.
* **Persistencia e Identificación Operativa:** *¡DESARROLLADO!* Las solicitudes confirmadas se graban en la base de datos local y se les asigna un Identificador único correlativo institucional con el formato `26/XXXX` (Año/Número).
* **Explotación del Manual de Usuario (RAG):** *[A DESARROLLAR A FUTURO]* Conexión del motor RAG (`rag_engine.py`) a la base vectorial para resolver dudas complejas sobre reparaciones de 1er y 2do escalón dentro del Flujo A.
* **Resguardo Criptográfico:** *[A DESARROLLAR A FUTURO]* Ofuscación simétrica de los datos sensibles de mantenimiento.

### 2. Logística y Compras (Épica 3)
* **Predicción de Insumos Críticos:** *[A DESARROLLAR A FUTURO]* Algoritmo encargado de predecir y generar automáticamente la lista optimizada de repuestos necesarios (formato `.xlsx`) en menos de 3 minutos por solicitud procesada.
* **Control de Stock y Alertas:** *[A DESARROLLAR A FUTURO]* Módulo de monitoreo de inventario en talleres con disparadores de alertas automáticas ante stock insuficiente o niveles críticos de repuestos de electrónica.

### 3. Monitoreo y Reportes (Épica 4)
* **Dashboard de Eficiencia Operativa:** *[A DESARROLLAR A FUTURO]* Panel de control para el seguimiento en tiempo real de los tiempos de reparación, configurado con alertas visuales automáticas si el proceso supera el 10% del tiempo estimado de mano de obra.
* **Módulo de Exportación Automatizada:** *[A DESARROLLAR A FUTURO]* Lógica alojada en `src/backend/utils/reports.py` para la generación dinámica de informes de gestión, partes diarios y reportes de estado en formatos PDF y Excel estandarizados por el EA.
```
