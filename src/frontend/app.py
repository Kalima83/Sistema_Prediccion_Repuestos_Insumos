import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="B Mant Com 601 - Asistente IA",
    page_icon="🤖",
    layout="wide"
)

# Título Principal
st.title("🤖 Sistema de Mantenimiento Asistido por IA")
st.markdown("---")

# Barra lateral informativa
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/561/561121.png", width=100)
st.sidebar.title("B Mant Com 601")
st.sidebar.info("Asistente técnico interactivo para gestión de repuestos, insumos y fallas en equipos de comunicaciones.")

# Dirección de nuestra API (FastAPI)
API_URL = "http://127.0.0.1:8000"

# Crear pestañas para separar los flujos
tab1, tab2 = st.tabs(["🔍 Consulta Técnica (RAG)", "📝 Cargar Solicitud de Reparación"])

# -------------------------------------------------------------------------
# FLUJO A: CONSULTA TÉCNICA (RAG)
# -------------------------------------------------------------------------
with tab1:
    st.header("Consulá los Manuales Técnicos")
    st.write("Escribí tu consulta sobre configuración o fallas comunes de los equipos de dotación.")
    
    pregunta = st.text_input("¿Qué necesitás saber?", placeholder="Ej: Deseo configurar una radio motorola GP 5050")
    
    if st.button("Buscar en Manuales", key="btn_consulta"):
        if pregunta.strip():
            with st.spinner("Buscando en la base de conocimientos..."):
                try:
                    res = requests.post(f"{API_URL}/consulta", json={"pregunta": pregunta})
                    if res.status_code == 200:
                        datos = res.json()
                        st.success("¡Respuesta encontrada!")
                        st.markdown(f"**Sistema:** {datos['respuesta_sistema']}")
                    else:
                        st.error("Hubo un error al procesar tu consulta en el servidor.")
                except Exception as e:
                    st.error(f"No se pudo conectar con la API. ¿Está el servidor encendido? (Detalle: {e})")
        else:
            st.warning("Por favor, escribí una pregunta antes de buscar.")

# -------------------------------------------------------------------------
# FLUJO B: CARGA DE SOLICITUD
# -------------------------------------------------------------------------
with tab2:
    st.header("Nueva Solicitud de Mantenimiento")
    st.write("Cargá los datos del equipo para validar la unidad y generar tu Número de Control.")

    col1, col2 = st.columns(2)
    
    with col1:
        unidad = st.text_input("Unidad Solicitante", placeholder="Ej: Comunicaciones Mecanizada 10")
    
    with col2:
        falla = st.text_input("Descripción de la Falla", placeholder="Ej: El equipo TRAN HARRIS HF RF tiene el ROE alto")

    if st.button("Registrar Solicitud", key="btn_solicitud"):
        if unidad.strip() and falla.strip():
            with st.spinner("Clasificando falla y validando unidad..."):
                try:
                    payload = {"unidad": unidad, "falla_descripcion": falla}
                    res = requests.post(f"{API_URL}/solicitud", json=payload)
                    
                    if res.status_code == 200:
                        datos = res.json()
                        st.balloons()  # ¡Efecto de globos para festejar el éxito!
                        st.success(f"🎉 **Solicitud procesada con éxito.**")
                        
                        # Tarjeta destacada con el Número de Control
                        st.metric(label="Número de Control Asignado", value=datos["nro_control"])
                        
                        # Detalle en cajitas limpias
                        st.markdown("### Detalles del Registro")
                        det = datos["detalle_procesado"]
                        st.json({
                            "Unidad Validada": det.get("unidad"),
                            "Código de Unidad": det.get("codigo_unidad"),
                            "Efecto a Reparar": det.get("efecto"),
                            "Código de Falla": det.get("codigo_falla"),
                            "Descripción Técnica": det.get("detalle_falla")
                        })
                    else:
                        st.error("Error del servidor al registrar la solicitud.")
                except Exception as e:
                    st.error(f"Error de conexión con la API: {e}")
        else:
            st.warning("Por favor, completá ambos campos antes de enviar.")