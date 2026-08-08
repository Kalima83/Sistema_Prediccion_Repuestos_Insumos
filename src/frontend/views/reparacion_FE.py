import streamlit as st
import requests
from fpdf import FPDF

API_URL = "http://127.0.0.1:8000"


def generar_pdf_bytes(data: dict) -> bytes:
    """Genera un comprobante oficial PDF binario en memoria sin desbordamientos de celda."""
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_margins(left=10, top=10, right=10)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Ancho imprimible A4: 210mm total - (10mm margen izq + 10mm margen der) = 190mm
    ANCHO_UTIL = 190

    # Encabezado estilo ticket técnico
    pdf.set_font("Courier", style="B", size=12)
    pdf.cell(ANCHO_UTIL, 6, "==================================================", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(ANCHO_UTIL, 6, "SOLICITUD DE MANTENIMIENTO DE ELECTRÓNICA", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.cell(ANCHO_UTIL, 6, "==================================================", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(4)

    # Extraer variables con fallbacks
    nro_ctl = data.get("nro_control") or data.get("nro_solicitud") # or "26/0000"
    unidad = data.get("unidad_nombre") or data.get("unidad") or "N/A"
    cod_uni = data.get("unidad_codigo") or data.get("codigo_unidad") or ""
    equipo = data.get("equipo_nombre") or data.get("efecto") or "N/A"
    ni = data.get("equipo_ni") or data.get("ni") or "S/NI"
    falla_tipo = data.get("falla_tipo") or data.get("tipo_falla") or "N/A"
    falla_cod = data.get("falla_codigo") or data.get("codigo_falla") or "N/A"
    detalle = data.get("descripcion_procesada") or data.get("detalle_falla") or "N/A"

    pdf.set_font("Courier", size=10)
    pdf.multi_cell(ANCHO_UTIL, 6, f"NRO DE CONTROL : {nro_ctl}", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(ANCHO_UTIL, 6, f"UNIDAD        : {unidad} (Cod: {cod_uni})", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(ANCHO_UTIL, 6, f"EQUIPO/EFECTO : {equipo} [NI: {ni}]", new_x="LMARGIN", new_y="NEXT")
    pdf.multi_cell(ANCHO_UTIL, 6, f"CÓDIGO FALLA  : {falla_cod} ({falla_tipo})", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_font("Courier", style="B", size=10)
    pdf.cell(ANCHO_UTIL, 6, "DETALLE TÉCNICO PROCESADO POR IA:", new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("Courier", size=9)
    pdf.multi_cell(ANCHO_UTIL, 5, str(detalle), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Courier", style="B", size=12)
    pdf.cell(ANCHO_UTIL, 6, "==================================================", new_x="LMARGIN", new_y="NEXT", align="C")

    return bytes(pdf.output())


def mostrar_interfaz():
    st.subheader("📝 Nueva Solicitud de Mantenimiento")

    if "form_key" not in st.session_state:
        st.session_state.form_key = 0
    if "traduccion_confirmada" not in st.session_state:
        st.session_state.traduccion_confirmada = False
    if "texto_traducido" not in st.session_state:
        st.session_state.texto_traducido = ""
    if "solicitud_guardada" not in st.session_state:
        st.session_state.solicitud_guardada = False
    if "datos_confirmados" not in st.session_state:
        st.session_state.datos_confirmados = {}

    k = st.session_state.form_key

    # VISTA POST-REGISTRO Y DESCARGA
    if st.session_state.solicitud_guardada:
        data_res = st.session_state.datos_confirmados
        nro_ctl = data_res.get("nro_control") or data_res.get("nro_solicitud") or "26/0000"
        
        st.balloons()
        st.success(f"¡Solicitud registrada con éxito! Número de Control oficial asignado: **{nro_ctl}**")
        
        # Muestra la información directamente en pantalla
        with st.expander("📄 Resumen de la Solicitud Confirmada", expanded=True):
            st.write(f"**N° Control:** {nro_ctl}")
            st.write(f"**Unidad:** {data_res.get('unidad_nombre', 'N/A')} ({data_res.get('unidad_codigo', 'N/A')})")
            st.write(f"**Equipo:** {data_res.get('equipo_nombre', 'N/A')} [NI: {data_res.get('equipo_ni', 'S/NI')}]")
            st.write(f"**Falla:** {data_res.get('falla_codigo', 'N/A')} - {data_res.get('falla_tipo', 'N/A')}")
            st.write(f"**Detalle Procesado:** {data_res.get('descripcion_procesada', 'N/A')}")

        # Generación segura del PDF
        try:
            pdf_bytes = generar_pdf_bytes(data_res)
        except Exception as e:
            pdf_bytes = b""
            st.error(f"Error generando PDF: {e}")

        col_pdf, col_fin = st.columns(2)
        with col_pdf:
            st.download_button(
                label="📄 Descargar Comprobante PDF",
                data=pdf_bytes,
                file_name=f"Comprobante_{str(nro_ctl).replace('/', '_')}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
                disabled=(pdf_bytes == b"")
            )

        with col_fin:
            if st.button("🏁 Finalizar y Cargar Nueva Solicitud", use_container_width=True):
                st.session_state.form_key += 1
                st.session_state.traduccion_confirmada = False
                st.session_state.texto_traducido = ""
                st.session_state.solicitud_guardada = False
                st.session_state.datos_confirmados = {}
                st.rerun()

        st.markdown("---")
        return

    # CARGA DE CATÁLOGOS DESDE EL BACKEND
    try:
        unidades_raw = requests.get(f"{API_URL}/reparacion/unidades").json()
        equipos_raw = requests.get(f"{API_URL}/reparacion/equipos").json()
        fallas_raw = requests.get(f"{API_URL}/reparacion/fallas").json()
    except Exception:
        st.error("⚠️ Error al conectar con la API REST Backend. Verifique la conexión.")
        unidades_raw, equipos_raw, fallas_raw = [], [], []

    dict_unidades = {u["nombre"]: u for u in unidades_raw if "nombre" in u} if unidades_raw else {}
    dict_equipos = {e["nombre"]: e for e in equipos_raw if "nombre" in e} if equipos_raw else {}
    dict_fallas = {f["tipo_falla"]: f for f in fallas_raw if "tipo_falla" in f} if fallas_raw else {}

    st.write("Completá los datos del equipo y describí el problema para generar el borrador técnico.")

    col1, col2 = st.columns(2)
    with col1:
        unidad_nombre_sel = st.selectbox(
            "Unidad Solicitante *",
            options=list(dict_unidades.keys()),
            index=None,
            placeholder="Seleccione la Unidad...",
            key=f"sel_unidad_{k}"
        )
        unidad_info = dict_unidades.get(unidad_nombre_sel) if unidad_nombre_sel else None
    
    with col2:
        equipo_nombre_sel = st.selectbox(
            "Equipo / Efecto (INE) *",
            options=list(dict_equipos.keys()),
            index=None,
            placeholder="Seleccione el Equipo/Efecto...",
            key=f"sel_equipo_{k}"
        )
        equipo_info = dict_equipos.get(equipo_nombre_sel) if equipo_nombre_sel else None

    col_nne, col_ni = st.columns(2)
    with col_nne:
        st.text_input("Número Nacional de Efecto (NNE)", value=equipo_info["nne"] if equipo_info else "", disabled=True)
    with col_ni:
        ni_usuario = st.text_input("Número de Identificación (NI) del equipo", key=f"input_ni_{k}")

    falla_tipo_sel = st.selectbox(
        "Descripción de la Falla Estándar *",
        options=list(dict_fallas.keys()),
        index=None,
        placeholder="Seleccione el tipo de falla...",
        key=f"sel_falla_{k}"
    )
    falla_info = dict_fallas.get(falla_tipo_sel) if falla_tipo_sel else None

    st.markdown("---")
    descripcion_libre = st.text_area("Describa detalladamente el problema: *", key=f"input_desc_{k}")

    if st.button("Procesar Descripción Técnica con IA", use_container_width=True):
        if not (unidad_info and equipo_info and falla_info and descripcion_libre.strip()):
            st.warning("Completá todos los campos requeridos (Unidad, Equipo, Falla y Descripción).")
        else:
            with st.spinner("Procesando con IA..."):
                try:
                    res = requests.post(f"{API_URL}/reparacion/traducir_falla", json={"texto_libre": descripcion_libre})
                    if res.status_code == 200:
                        st.session_state.texto_traducido = res.json()["texto_traducido"]
                        st.session_state.traduccion_confirmada = True
                        st.rerun()
                    else:
                        st.error("⚠️ Error de procesamiento. Pruebe en unos momentos.")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")

    # PREVISUALIZACIÓN Y REGISTRO
    if st.session_state.traduccion_confirmada and unidad_info and equipo_info and falla_info:
        st.markdown("---")
        st.subheader("📋 Previsualización del Ticket")
        
        ticket_html = f"""<div style="border: 2px dashed #0E8388; padding: 20px; border-radius: 8px; background-color: #f9fbfb; font-family: monospace;">
<h4>SOLICITUD DE MANTENIMIENTO DE ELECTRÓNICA</h4>
<p><b>NRO CONTROL:</b> [Se asignará al guardar de forma atómica]</p>
<p><b>UNIDAD:</b> {unidad_info['nombre']} ({unidad_info['codigo']})</p>
<p><b>EQUIPO:</b> {equipo_info['nombre']} | <b>NI:</b> {ni_usuario or 'S/NI'}</p>
<p><b>CÓDIGO FALLA:</b> {falla_info['codigo_falla']} ({falla_info['tipo_falla']})</p>
<p><b>DETALLE TÉCNICO IA:</b> {st.session_state.texto_traducido}</p>
</div>"""
        st.markdown(ticket_html, unsafe_allow_html=True)

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("Confirmar y Dar de Alta Solicitud", type="primary", use_container_width=True):
                payload = {
                    "unidad_nombre": unidad_info["nombre"],
                    "unidad_abreviatura": unidad_info["abreviatura"],
                    "unidad_codigo": str(unidad_info["codigo"]),
                    "equipo_nombre": equipo_info["nombre"],
                    "equipo_nne": str(equipo_info["nne"]),
                    "equipo_ni": ni_usuario if ni_usuario else "S/NI",
                    "falla_tipo": falla_info["tipo_falla"],
                    "falla_codigo": str(falla_info["codigo_falla"]),
                    "descripcion_procesada": st.session_state.texto_traducido
                }
                try:
                    with st.spinner("Registrando solicitud..."):
                        res_guardar = requests.post(f"{API_URL}/reparacion/solicitud", json=payload)
                        
                        if res_guardar.status_code == 200:
                            st.session_state.datos_confirmados = {**payload, **res_guardar.json()}
                            st.session_state.solicitud_guardada = True
                            st.rerun()
                        else:
                            st.error("⚠️ Error de carga. El sistema se encuentra procesando otras solicitudes, por favor intente de nuevo en unos momentos.")
                except Exception:
                    st.error("⚠️ No se pudo conectar con el servidor. Pruebe en unos momentos.")

        with btn2:
            if st.button("Cancelar / Modificar Borrador", use_container_width=True):
                st.session_state.traduccion_confirmada = False
                st.session_state.texto_traducido = ""
                st.rerun()