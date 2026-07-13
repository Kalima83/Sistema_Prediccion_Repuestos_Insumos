import sqlite3
import os

# Ruta a la base de datos en la raíz del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "sistema_mantenimiento.db")

def inicializar_base_datos():
    """Crea las tablas necesarias para el historial y el aprendizaje si no existen."""
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    # 1. Tabla de Solicitudes de Mantenimiento (Flujo B)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nro_control TEXT UNIQUE,
            codigo_unidad TEXT,
            unidad TEXT,
            efecto TEXT,
            codigo_falla TEXT,
            detalle_falla TEXT,
            estado TEXT DEFAULT 'Pendiente',
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Tabla de Historial de Conversaciones (Para que el bot aprenda del Técnico)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_conversaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id TEXT,
            remitente TEXT, -- 'Usuario', 'Chatbot' o 'Tecnico'
            mensaje TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conexion.commit()
    conexion.close()
    print("Base de datos local inicializada correctamente.")

if __name__ == "__main__":
    inicializar_base_datos()