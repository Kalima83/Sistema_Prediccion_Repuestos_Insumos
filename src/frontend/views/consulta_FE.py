import streamlit as st
import requests

def mostrar_interfaz():
    # Textos idénticos a tu diseño original
    st.subheader("Consulá los Manuales Técnicos")
    st.write("Escribí tu consulta sobre configuración o fallas comunes de los equipos de dotación.")
    
    pregunta = st.text_input("¿Qué necesitás saber?", placeholder="Ej: Deseo configurar una radio motorola GP 5050")
    
    if st.button("Buscar en Manuales"):
        if pregunta:
            with st.spinner("Buscando en la base de datos técnica..."):
                try:
                    # Conectamos con el Backend
                    respuesta = requests.post(
                        "http://127.0.0.1:8000/consulta/",
                        json={"pregunta": pregunta}
                    )
                    if respuesta.status_code == 200:
                        datos = respuesta.json()
                        st.success("Búsqueda completada")
                        st.info(f"**Respuesta del Sistema:**\n\n{datos['respuesta_sistema']}")
                    else:
                        st.error("Hubo un error al procesar la consulta en el servidor.")
                except requests.exceptions.ConnectionError:
                    st.error("No se pudo conectar con el servidor Backend. Verificá que Uvicorn esté corriendo.")
        else:
            st.warning("Por favor, ingresá una pregunta.")