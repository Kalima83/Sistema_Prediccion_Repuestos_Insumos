import streamlit as st
from views import consulta_FE, reparacion_FE

# Configuración global de la página
st.set_page_config(page_title="Sistema Logístico 601", layout="wide", page_icon="⚙️")

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    # Cuando tengas el logo, descomentá la línea de abajo y poné la ruta correcta:
    # st.image("ruta/al/logo_batallon.png", width=150)
    st.markdown("### 🛡️ [Logo del Batallón]") 
    st.title("B Mant Com 601")
    st.info("Asistente técnico interactivo para gestión de repuestos, insumos y fallas en equipos de comunicaciones.")

# --- TÍTULO PRINCIPAL ---
st.title("🤖 Sistema de Mantenimiento de Electrónica Asistido por IA")
st.markdown("---")

# --- NAVEGACIÓN POR PESTAÑAS (TABS) ---
# Esto recrea exactamente el menú superior que tenías en la imagen
tab_consulta, tab_reparacion = st.tabs(["🔍 Consulta Técnica", "📝 Cargar Solicitud de Reparación"])

# Ruteo visual del contenido
with tab_consulta:
    consulta_FE.mostrar_interfaz()

with tab_reparacion:
    reparacion_FE.mostrar_interfaz()