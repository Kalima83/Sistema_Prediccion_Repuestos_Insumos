import sqlite3
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

# Garantizar ruta a data/sistema_mantenimiento.db
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = str(DATA_DIR / "sistema_mantenimiento.db")


def inicializar_db_indice():
    """Crea la tabla de índice y asignación si no existe."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS indice_tickets (
                nro_control TEXT PRIMARY KEY,
                ruta_ticket TEXT NOT NULL,
                unidad_nombre TEXT,
                equipo_nombre TEXT,
                falla_codigo TEXT,
                estado TEXT DEFAULT 'Pendiente',
                operador_asignado TEXT DEFAULT 'Sin Asignar',
                taller_asignado TEXT DEFAULT 'Laboratorio Electrónica Central',
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Inicializamos al importar el módulo
inicializar_db_indice()


def obtener_y_incrementar_nro_control(prefijo: str = "26") -> str:
    """Genera el siguiente correlativo atómico directamente con SQLite."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM indice_tickets WHERE nro_control LIKE ?", (f"{prefijo}/%",))
        total = cursor.fetchone()[0]
        proximo = total + 1
        return f"{prefijo}/{proximo:04d}"


def registrar_nro_control_indice(
    nro_control: str,
    ruta_ticket: str,
    unidad_nombre: str,
    equipo_nombre: str,
    falla_codigo: str,
    taller_asignado: str = "Laboratorio Electrónica Central"
):
    """Inserta el nuevo ticket en el índice SQLite de rápida consulta."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO indice_tickets (
                nro_control, ruta_ticket, unidad_nombre, equipo_nombre, 
                falla_codigo, estado, operador_asignado, taller_asignado
            ) VALUES (?, ?, ?, ?, ?, 'Pendiente', 'Sin Asignar', ?)
        ''', (nro_control, ruta_ticket, unidad_nombre, equipo_nombre, falla_codigo, taller_asignado))
        conn.commit()


def actualizar_asignacion_y_estado(
    nro_control: str,
    estado: str,
    taller_asignado: str,
    operador_asignado: str
):
    """Permite al supervisor o revisor asignar un operario y cambiar estado."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE indice_tickets
            SET estado = ?, taller_asignado = ?, operador_asignado = ?
            WHERE nro_control = ?
        ''', (estado, taller_asignado, operador_asignado, nro_control))
        conn.commit()


def listar_indice_tickets(filtro_operador: Optional[str] = None) -> List[Dict[str, Any]]:
    """Consulta rápida para el supervisor o los operarios."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if filtro_operador == "Sin Asignar":
            cursor.execute("SELECT * FROM indice_tickets WHERE operador_asignado = 'Sin Asignar' ORDER BY fecha_creacion DESC")
        elif filtro_operador:
            cursor.execute("SELECT * FROM indice_tickets WHERE operador_asignado = ? ORDER BY fecha_creacion DESC", (filtro_operador,))
        else:
            cursor.execute("SELECT * FROM indice_tickets ORDER BY fecha_creacion DESC")
            
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def consultar_nro_control(nro_control: str) -> dict:
    """Verifica si existe el número y retorna su ruta física o datos básicos."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM indice_tickets WHERE nro_control = ?", (nro_control,))
        row = cursor.fetchone()
        
        if not row:
            return {"existe": False, "mensaje": "Número de Control inexistente"}
            
        data_indice = dict(row)
        ruta_ticket = data_indice["ruta_ticket"]
        
        if not os.path.exists(ruta_ticket):
            return {"existe": False, "mensaje": f"El ticket {nro_control} figura en el índice pero no se halló su archivo binario."}

        import pickle
        with open(ruta_ticket, "rb") as f:
            datos_completos = pickle.load(f)
            # Combinar datos completos con la asignación actual
            datos_completos.update(data_indice)

        return {"existe": True, "datos": datos_completos}