import os
from pathlib import Path
from dotenv import load_dotenv

# Encontrar la ruta del directorio raíz
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar el archivo .env
load_dotenv(BASE_DIR / ".env")

class Settings:
    # Generales
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "True").lower() == "true"
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-default")

    # Base de datos vectorial
    VECTOR_DB_URL: str = os.getenv("VECTOR_DB_URL", "http://localhost:6333")

    # Base de datos relacional
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", 5432))
    DB_NAME: str = os.getenv("DB_NAME", "ea_logistica_db")
    DB_USER: str = os.getenv("DB_USER", "postgres_ea")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "secret")

    # Configuración de IA (local)
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "ollama")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3:8b")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-minilm")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    # Reglas de negocio (Historias de Usuario)
    UMBRAL_ALERTA_TIEMPO: float = float(os.getenv("UMBRAL_ALERTA_TIEMPO", 0.10))

# Instancia global para importar en el resto del código
settings = Settings()
