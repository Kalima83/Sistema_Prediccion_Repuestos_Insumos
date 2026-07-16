import streamlit as st
import os

# Configuración global de la página
st.set_page_config(page_title="Sistema Logístico 601", layout="wide", page_icon="⚙️")

# --- CONTROL DE RUTAS ABSOLUTAS ---
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_LOGO = os.path.join(DIRECTORIO_ACTUAL, "assets", "escudo_bmant.png")
RUTA_FONDO = os.path.join(DIRECTORIO_ACTUAL, "assets", "fondo_bamant.png") 

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
<style>
    /* Fondo general claro */
    .stApp {
        background-color: #f4f6f9;
    }
    /* Contenedor principal estilizado como tarjeta */
    .block-container {
        background-color: #ffffff;
        padding: 2rem 2.5rem !important;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # 1. Logo del Batallón arriba de todo en el sidebar
    if os.path.exists(RUTA_LOGO):
        st.image(RUTA_LOGO, width=150)
    else:
        st.title("🛡️") # Resguardo visual
    
    # 2. Información Institucional completa
    st.title("Sistema de Mantenimiento de Electrónica Asistido por IA")
    st.subheader("Batallón de Mantenimiento de Comunicaciones 601 - DGCICD")
    st.info("Asistente técnico interactivo para gestión de repuestos, insumos y fallas en equipos de comunicaciones.")

# --- CUERPO PRINCIPAL ---

# 1. Imagen de cabecera arriba de todo
if os.path.exists(RUTA_FONDO):
    st.image(RUTA_FONDO, use_container_width=True)
else:
    st.info("📷 Guardá 'fondo_bamant.jpg' en la carpeta assets.")

# 2. Título secundario abajo de la imagen
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("⚙️ Sistema Logístico para Mantenimiento de Electrónica")
st.markdown("---")

# Importación diferida de las vistas
from views import consulta_FE, reparacion_FE

# --- NAVEGACIÓN POR PESTAÑAS (TABS) ---
tab_consulta, tab_reparacion = st.tabs(["🔍 Consulta Técnica", "📝 Cargar Solicitud de Reparación"])

with tab_consulta:
    consulta_FE.mostrar_interfaz()

with tab_reparacion:
    reparacion_FE.mostrar_interfaz()