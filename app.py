import importlib
import streamlit as st
import estilos
import funciones
import vistas

# Recarga automatica de los modulos secundarios al guardar cambios en vivo
importlib.reload(estilos)
importlib.reload(funciones)
importlib.reload(vistas)

st.set_page_config(
    page_title="Presentacion DEIS-REM - Cancer de Mama",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

estilos.aplicar_estilos_dashboard()

# Menu lateral izquierdo limpio con Design System "Clinico limpio"
with st.sidebar:
    st.markdown(
        """
        <div style="padding: 10px 6px 20px 6px;">
            <div style="font-size: 20px; font-weight: 800; letter-spacing: -0.03em; color: #0C2340;">
                DEIS-REM
            </div>
            </div>

        """,
        unsafe_allow_html=True,
    )

    opciones_menu = [
        "Tablas",
        "Exploración",
        "Analisis e Impacto",
    ]

    seccion_seleccionada = st.radio(
        "Seleccione una vista",
        opciones_menu,
        label_visibility="collapsed",
    )

# Encabezado superior del panel principal
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: left; margin-bottom: 3px; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="font-size: 20px; font-weight: 600; letter-spacing: 0.04em; color: #6D7B8C; line-height: 1.15; margin-bottom: 30px;">
                Exploracion y Analisis con Datos DEIS-REM
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Renderizado de la vista activa segun el menu lateral
if seccion_seleccionada == "Tablas":
    vistas.renderizar_pestana_tablas()
elif seccion_seleccionada == "Exploración":
    vistas.renderizar_pestana_busqueda()
elif seccion_seleccionada == "Analisis e Impacto":
    vistas.renderizar_pestana_analisis_mama()
