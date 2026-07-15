import os
import sqlite3
from typing import Dict, Any, Optional
from src.backend.core.procesamiento_inventario import cargar_unidades, procesar_efectos, cargar_fallas_estandarizadas

# Ruta a la base de datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "sistema_mantenimiento.db")

class ChatbotMantenimiento:
    def __init__(self):
        print("Inicializando componentes del Chatbot (B Mant Com 601)...")
        self.unidades = cargar_unidades()
        self.efectos = procesar_efectos()
        self.fallas = cargar_fallas_estandarizadas()

    def saludar_usuario(self) -> str:
        return (
            "==========================================================\n"
            "Usted se ha comunicado con el B Mant Com 601.\n"
            "Por favor, seleccione una opción para continuar:\n"
            "  A) Realizar una CONSULTA TÉCNICA sobre un equipo.\n"
            "  B) Solicitar MANTENIMIENTO para un efecto de electrónica.\n"
            "=========================================================="
        )

    def buscar_unidad_flexible(self, entrada_usuario: str) -> Optional[Dict]:
        termino = entrada_usuario.strip().lower()
        if not termino:
            return None

        for u in self.unidades:
            if u["codigo_u"].lower() == termino:
                return u

        for u in self.unidades:
            nombre = u["nombre_unidad"].lower()
            abreviatura = str(u.get("abreviatura", "")).lower()
            if termino in nombre or (abreviatura and termino in abreviatura):
                return u
        return None

    def simular_flujo_consulta_rag(self, pregunta_tecnica: str) -> str:
        print(f"\n[Ejecutando Pipeline PLN + RAG para]: '{pregunta_tecnica}'")
        respuesta_contexto = (
            "-> [RAG - Manual]: Para mitigar la incertidumbre o fallas de enlace, "
            "verifique los parámetros del canal y la zona en el manual de usuario."
        )
        return respuesta_contexto

    def generar_proximo_numero_control(self) -> str:
        """Calcula el correlativo real consultando la base de datos (Formato 26/XXXX)"""
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        # Contamos cuántas solicitudes existen en el año actual (2026)
        cursor.execute("SELECT COUNT(*) FROM solicitudes WHERE nro_control LIKE '26/%'")
        total_año = cursor.fetchone()[0]
        conexion.close()
        
        proximo_id = total_año + 1
        nro_formateado = str(proximo_id).zfill(4)
        return f"26/{nro_formateado}"

    def procesar_y_guardar_solicitud(self, dato_unidad: str, texto_falla: str) -> Dict[str, Any]:
        """Flujo B: Clasifica los datos, genera el Nro de Control y los persiste en SQLite."""
        unidad_detectada = self.buscar_unidad_flexible(dato_unidad)
        
        # Búsqueda de efecto y falla por subcadenas
        efecto_detectado = None
        texto_falla_min = texto_falla.lower()
        for e in self.efectos:
            if e["ine"].lower() in texto_falla_min:
                efecto_detectado = e
                break

        falla_detectada = None
        for f in self.fallas:
            if f["falla_estandar"].lower() in texto_falla_min or f["referencia_sintomas"].lower() in texto_falla_min:
                falla_detectada = f
                break

        # Asignamos variables finales
        nro_control = self.generar_proximo_numero_control()
        cod_u = unidad_detectada["codigo_u"] if unidad_detectada else "NO_IDENTIFICADO"
        nom_u = unidad_detectada["nombre_unidad"] if unidad_detectada else dato_unidad
        efecto = efecto_detectado["ine"] if efecto_detectado else "A evaluar"
        cod_f = falla_detectada["codigo_falla"] if falla_detectada else "999"
        det_f = falla_detectada["falla_estandar"] if falla_detectada else texto_falla

        # Guardamos en la Base de Datos de manera real
        try:
            conexion = sqlite3.connect(DB_PATH)
            cursor = conexion.cursor()
            cursor.execute('''
                INSERT INTO solicitudes (nro_control, codigo_unidad, unidad, efecto, codigo_falla, detalle_falla)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nro_control, cod_u, nom_u, efecto, cod_f, det_f))
            conexion.commit()
            conexion.close()
            guardado_ok = True
        except Exception as e:
            print(f"Error al persistir solicitud: {e}")
            guardado_ok = False

        return {
            "nro_control": nro_control,
            "guardado_exitoso": guardado_ok,
            "unidad_validada": unidad_detectada is not None,
            "datos_solicitud": {
                "codigo_unidad": cod_u,
                "unidad": nom_u,
                "efecto": efecto,
                "codigo_falla": cod_f,
                "detalle_falla": det_f
            }
        }