import streamlit as st

# ==============================================================================
# SELECTOR RAPIDO DE PALETA DE COLORES
# Opciones disponibles: "clinico_limpio", "bento_pastel", "editorial_rosa", "institucional_salud"
# ==============================================================================

PALETA_ELEGIDA = "clinico_limpio"

PALETAS_PREDEFINIDAS = {
    "clinico_limpio": {
        "color_fondo_pagina": "#F7FAFC",
        "color_superficie_suave": "#DBE8F3",
        "color_azul_clinico": "#2E6B8A",
        "color_tinta": "#0C2340",
        "color_rosa_apagado": "#C46D85",
        "color_superficie_rosa": "#F4E3E8",
        "color_fondo_sidebar": "#FFFFFF",
        "color_fondo_tarjetas": "#FFFFFF",
        "color_borde_tarjetas": "#DBE8F3",
        "color_titulo_principal": "#0C2340",
        "color_encabezado_seccion": "#0C2340",
        "color_subtitulo": "#2E6B8A",
        "color_texto_general": "#0C2340",
        "color_acento_menu": "#2E6B8A",
        "color_texto_menu_activo": "#FFFFFF",
        "color_fondo_menu_hover": "#DBE8F3",
        "color_grafico_primario": "#2E6B8A",
        "color_grafico_secundario": "#7FAAC2",
        "color_grafico_alerta": "#C46D85",
        "color_sombreado_cuarentena": "rgba(196, 109, 133, 0.18)",
        "color_anotacion_minimo": "#0C2340",
        "color_linea_referencia": "#0C2340",
    },
    "bento_pastel": {
        "color_fondo_pagina": "#F6F4EE",
        "color_superficie_suave": "#BFD4F2",
        "color_azul_clinico": "#1F5E3B",
        "color_tinta": "#18181B",
        "color_rosa_apagado": "#D96B98",
        "color_superficie_rosa": "#F5C6DF",
        "color_fondo_sidebar": "#FFFFFF",
        "color_fondo_tarjetas": "#FFFFFF",
        "color_borde_tarjetas": "#E8E4DC",
        "color_titulo_principal": "#18181B",
        "color_encabezado_seccion": "#1F2937",
        "color_subtitulo": "#374151",
        "color_texto_general": "#27272A",
        "color_acento_menu": "#1F5E3B",
        "color_texto_menu_activo": "#FFFFFF",
        "color_fondo_menu_hover": "#F3F4F6",
        "color_grafico_primario": "#1F5E3B",
        "color_grafico_secundario": "#7E99A3",
        "color_grafico_alerta": "#D96B98",
        "color_sombreado_cuarentena": "rgba(245, 198, 223, 0.45)",
        "color_anotacion_minimo": "#18181B",
        "color_linea_referencia": "#18181B",
    },
    "editorial_rosa": {
        "color_fondo_pagina": "#FCF7F7",
        "color_superficie_suave": "#F4E3E8",
        "color_azul_clinico": "#6E1D47",
        "color_tinta": "#3D0E2A",
        "color_rosa_apagado": "#B8335A",
        "color_superficie_rosa": "#F8E5EA",
        "color_fondo_sidebar": "#FFFFFF",
        "color_fondo_tarjetas": "#FFFFFF",
        "color_borde_tarjetas": "#EED6DA",
        "color_titulo_principal": "#3D0E2A",
        "color_encabezado_seccion": "#6E1D47",
        "color_subtitulo": "#8C2D56",
        "color_texto_general": "#2B1E24",
        "color_acento_menu": "#8C2D56",
        "color_texto_menu_activo": "#FFFFFF",
        "color_fondo_menu_hover": "#FDF2F4",
        "color_grafico_primario": "#2B5B84",
        "color_grafico_secundario": "#6C8EAD",
        "color_grafico_alerta": "#B8335A",
        "color_sombreado_cuarentena": "rgba(184, 51, 90, 0.16)",
        "color_anotacion_minimo": "#6E1D47",
        "color_linea_referencia": "#4A3540",
    },
    "institucional_salud": {
        "color_fondo_pagina": "#F7F9FC",
        "color_superficie_suave": "#DBE8F3",
        "color_azul_clinico": "#1B4965",
        "color_tinta": "#0F2C59",
        "color_rosa_apagado": "#D1495B",
        "color_superficie_rosa": "#F6E4E7",
        "color_fondo_sidebar": "#FFFFFF",
        "color_fondo_tarjetas": "#FFFFFF",
        "color_borde_tarjetas": "#DCE4F0",
        "color_titulo_principal": "#0F2C59",
        "color_encabezado_seccion": "#1B4965",
        "color_subtitulo": "#2B5B84",
        "color_texto_general": "#1F2933",
        "color_acento_menu": "#1B4965",
        "color_texto_menu_activo": "#FFFFFF",
        "color_fondo_menu_hover": "#EDF2F7",
        "color_grafico_primario": "#1D6396",
        "color_grafico_secundario": "#5FA8D3",
        "color_grafico_alerta": "#D1495B",
        "color_sombreado_cuarentena": "rgba(209, 73, 91, 0.16)",
        "color_anotacion_minimo": "#8B1E2B",
        "color_linea_referencia": "#334155",
    },
}

paleta_base = PALETAS_PREDEFINIDAS[PALETA_ELEGIDA]

CONFIGURACION_ESTILO = {
    # Tipografia del Design System "Clinico limpio"
    # --font-sans: "Manrope", ui-sans-serif, system-ui, sans-serif #light: 300, regular: 400, medium: 500, bold: 700
    # --font-mono: "IBM Plex Mono", ui-monospace, monospace
    "familia_fuente": '"Manrope", extralight, ui-sans-serif, system-ui, sans-serif',
    "familia_fuente_mono": '"IBM Plex Mono", ui-monospace, monospace',

    # Tamanos de letra en la interfaz web
    "tamano_titulo_principal": "58px",
    "tamano_encabezado_seccion": "35px",
    "tamano_subtitulo": "25px",
    "tamano_texto_general": "18px",
    "tamano_etiqueta_caption": "15px",
    "tamano_menu_lateral": "12px",
    "tamano_barra_horizontal": "12px",
    "ancho_menu_lateral": "130px",
    "tamano_codigo": "9px",

    # Configuracion de tamano de textos de la Ruta Clinica
    "tamano_titulo_ruta_clinica": "18px",
    "tamano_texto_ruta_clinica": "13px",
    "tamano_pildora_ruta_clinica": "14px",
    "tamano_pildora_birads": "12px",

    # Configuracion de las tablas de esquema (columna, tipo, descripcion)
    "tamano_letra_tabla_esquema": "12px",
    "relleno_fila_tabla_esquema": "8px 14px",
    "altura_maxima_tabla_esquema": "none",
    "ancho_tabla_esquema": "75%",

    # Configuracion independiente de la tabla de consolidacion historica (Analisis e Impacto)
    "tamano_letra_tabla_consolidacion": "9px",
    "relleno_fila_tabla_consolidacion": "4px 5px",
    "altura_maxima_tabla_consolidacion": "none",
    "ancho_tabla_consolidacion": "fit-content",

    # Configuracion de tamano, ancho y colores de las vistas de tablas de ejemplo
    "tamano_letra_tabla": "12px",
    "relleno_fila_tabla": "10px 16px",
    "altura_maxima_tabla": "445px",
    "proporcion_columnas_codigo_tabla": [0.60, 1.90],
    "proporcion_tarjetas_ruta_clinica": [1.0, 1.65, 1.0, 0.95],
    "separacion_columnas": "40px",
    "usar_tabla_html_escalable": True,
    "color_fondo_encabezado_tabla": paleta_base["color_superficie_suave"],
    "color_texto_encabezado_tabla": paleta_base["color_tinta"],

    # Radio de redondeo de las tarjetas estilo Bento
    "radio_borde_tarjetas": "24px",

    # Alineacion de titulos ("left", "center" o "right")
    "alineacion_titulo_principal": "left",
    "alineacion_encabezado_seccion": "center",
    "alineacion_subtitulo": "left",

    # Colores del Design System cargados desde la paleta elegida
    "color_fondo_pagina": paleta_base["color_fondo_pagina"],
    "color_superficie_suave": paleta_base["color_superficie_suave"],
    "color_azul_clinico": paleta_base["color_azul_clinico"],
    "color_tinta": paleta_base["color_tinta"],
    "color_rosa_apagado": paleta_base["color_rosa_apagado"],
    "color_superficie_rosa": paleta_base["color_superficie_rosa"],
    "color_fondo_sidebar": paleta_base["color_fondo_sidebar"],
    "color_fondo_tarjetas": paleta_base["color_fondo_tarjetas"],
    "color_borde_tarjetas": paleta_base["color_borde_tarjetas"],
    "color_titulo_principal": paleta_base["color_titulo_principal"],
    "color_encabezado_seccion": paleta_base["color_encabezado_seccion"],
    "color_subtitulo": paleta_base["color_subtitulo"],
    "color_texto_general": paleta_base["color_texto_general"],
    "color_acento_menu": paleta_base["color_acento_menu"],
    "color_texto_menu_activo": paleta_base["color_texto_menu_activo"],
    "color_fondo_menu_hover": paleta_base["color_fondo_menu_hover"],

    # Colores y parametros de los graficos Plotly
    "color_grafico_primario": paleta_base["color_grafico_primario"],
    "color_grafico_secundario": paleta_base["color_grafico_secundario"],
    "color_grafico_alerta": paleta_base["color_grafico_alerta"],
    "color_sombreado_cuarentena": paleta_base["color_sombreado_cuarentena"],
    "color_anotacion_minimo": paleta_base["color_anotacion_minimo"],
    "color_linea_referencia": paleta_base["color_linea_referencia"],
    "plantilla_plotly": "plotly_white",
    "tamano_titulo_grafico": 20,
    "tamano_ejes_grafico": 14,
    "altura_grafico": 430,
}


def aplicar_estilos_dashboard():
    """
    Inyecta las reglas CSS en Streamlit tomando los valores definidos
    en CONFIGURACION_ESTILO para aplicar el Design System 'Clinico limpio'
    con las fuentes Manrope e IBM Plex Mono.
    """
    estilo = CONFIGURACION_ESTILO
    columnas_ruta_css = " ".join(
        f"minmax(0, {valor}fr)"
        for valor in estilo.get("proporcion_tarjetas_ruta_clinica", [1.0, 1.65, 1.0, 0.95])
    )

    bloque_css = f"""<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {{
    --font-sans: {estilo["familia_fuente"]};
    --font-mono: {estilo["familia_fuente_mono"]};
}}

header[data-testid="stHeader"] {{
    background: transparent !important;
    height: 0px !important;
    min-height: 0px !important;
    padding: 0 !important;
    overflow: visible !important;
}}

[data-testid="stToolbarActions"],
[data-testid="stAppDeployButton"],
[data-testid="stMainMenu"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {{
    display: none !important;
}}

[data-testid="stExpandSidebarButton"],
[data-testid="collapsedControl"] {{
    display: flex !important;
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 999999 !important;
    background-color: {estilo["color_superficie_suave"]} !important;
    border-radius: 10px !important;
}}

html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background-color: {estilo["color_fondo_pagina"]} !important;
    font-family: {estilo["familia_fuente"]} !important;
    color: {estilo["color_texto_general"]} !important;
}}

.block-container,
[data-testid="stMainBlockContainer"] {{
    padding-top: 0.5rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2.8rem !important;
    padding-right: 2.8rem !important;
    max-width: 100% !important;
}}

[data-testid="stHorizontalBlock"] {{
    gap: {estilo["separacion_columnas"]} !important;
}}

@media (min-width: 641px) {{
    [data-testid="stHorizontalBlock"] {{
        flex-wrap: nowrap !important;
    }}

    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {{
        min-width: 0 !important;
    }}
}}

/* Ocultar circulo de radio button en todos los selectores de navegacion */
div[role="radiogroup"] label > div:first-child,
div[role="radiogroup"] label > span:first-child {{
    display: none !important;
}}

div[role="radiogroup"] input[type="radio"] {{
    appearance: none !important;
    -webkit-appearance: none !important;
    position: absolute !important;
    opacity: 0 !important;
    width: 0 !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    pointer-events: none !important;
}}

/* Menu lateral izquierdo (Sidebar vertical) */
section[data-testid="stSidebar"] {{
    background-color: {estilo["color_fondo_sidebar"]} !important;
    border-right: 1px solid {estilo["color_borde_tarjetas"]} !important;
}}

section[data-testid="stSidebar"][aria-expanded="true"],
section[data-testid="stSidebar"][data-collapsed="false"] {{
    width: {estilo["ancho_menu_lateral"]} !important;
    min-width: {estilo["ancho_menu_lateral"]} !important;
    max-width: {estilo["ancho_menu_lateral"]} !important;
}}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"],
section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
section[data-testid="stSidebar"] .block-container {{
    padding-left: 2px !important;
    padding-right: 2px !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] {{
    gap: 10px !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label {{
    width: 100% !important;
    padding: 10px 2px !important;
    border-radius: 24px !important;
    margin: 0 !important;
    cursor: pointer !important;
    transition: all 0.18s ease-in-out !important;
    border: 1px solid transparent !important;
    background-color: transparent !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
    background-color: {estilo["color_fondo_menu_hover"]} !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label,
section[data-testid="stSidebar"] div[role="radiogroup"] label p,
section[data-testid="stSidebar"] div[role="radiogroup"] label span,
section[data-testid="stSidebar"] div[role="radiogroup"] label div {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_menu_lateral"]} !important;
    font-weight: 500 !important;
    color: {estilo["color_tinta"]} !important;
    margin: 0 !important;
    word-break: normal !important;
    overflow-wrap: normal !important;
    white-space: normal !important;
    line-height: 1.35 !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {{
    background-color: {estilo["color_acento_menu"]} !important;
    box-shadow: 0 4px 12px rgba(46, 107, 138, 0.22) !important;
}}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked),
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) span,
section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) div {{
    color: {estilo["color_texto_menu_activo"]} !important;
    font-weight: 500 !important;
}}

/* Barra de navegacion horizontal interna (Sidebar horizontal en la vista de tablas) */
.block-container [data-testid="stElementContainer"]:has(div[role="radiogroup"]),
.block-container .stRadio,
.block-container [data-testid="stRadio"],
.block-container [data-testid="stRadio"] > div {{
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    min-height: 0 !important;
}}

.block-container div[role="radiogroup"] {{
    align-items: center !important;
    background-color: #FFFFFF !important;
    border: 2px solid #2E6B8A !important;
    padding: 4px !important;
    border-radius: 24px !important;
    display: inline-flex !important;
    flex-direction: row !important;
    flex-wrap: wrap !important;
    justify-content: center !important;
    gap: 8px !important;
    margin: 0 auto !important;
    width: fit-content !important;
}}

.block-container div[role="radiogroup"] label {{
    display: inline-flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 6px 22px !important;
    border-radius: 20px !important;
    margin: 4px !important;
    cursor: pointer !important;
    transition: all 0.18s ease-in-out !important;
    background-color: transparent !important;
}}

.block-container div[role="radiogroup"] label:hover {{
    background-color: rgba(255, 255, 255, 0.55) !important;
}}

.block-container div[role="radiogroup"] label > div:last-child,
.block-container div[role="radiogroup"] label [data-testid="stMarkdownContainer"] {{
    padding: 0 !important;
    margin: 0 !important;
}}

.block-container div[role="radiogroup"] label p {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_barra_horizontal"]} !important;
    font-weight: 400 !important;
    text-align: center !important;
    color: {estilo["color_tinta"]} !important;
    margin: 0 !important;
    padding: 0 !important;
    line-height: 1.2 !important;
}}

.block-container div[role="radiogroup"] label:has(input:checked) {{
    background-color: {estilo["color_azul_clinico"]} !important;
    box-shadow: 0 3px 10px rgba(12, 35, 64, 0.16) !important;
}}

.block-container div[role="radiogroup"] label:has(input:checked) p {{
    color: #FFFFFF !important;
    font-weight: 500 !important;
}}

/* Ocultar el span vacio del icono de ancla en los titulos y etiquetas colapsadas */
[data-testid="stHeaderActionElements"],
h1 a, h2 a, h3 a,
.stRadio [data-testid="stWidgetLabel"],
[data-testid="stRadio"] [data-testid="stWidgetLabel"] {{
    display: none !important;
}}

/* Encabezados y textos */
h1, [data-testid="stHeadingWithActionElements"] h1, [data-testid="stHeading"] h1 {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_titulo_principal"]} !important;
    font-weight: 600 !important;
    letter-spacing: -0.025em !important;
    color: {estilo["color_titulo_principal"]} !important;
    text-align: {estilo["alineacion_titulo_principal"]} !important;
    width: 100% !important;
    padding-bottom: 0.2rem !important;
    margin-bottom: 0 !important;
}}



h2, [data-testid="stHeadingWithActionElements"] h2, [data-testid="stHeading"] h2 {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_encabezado_seccion"]} !important;
    font-weight: 600 !important;
    letter-spacing: 0.01em !important;
    color: {estilo["color_encabezado_seccion"]} !important;
    text-align: {estilo["alineacion_encabezado_seccion"]} !important;
    width: 100% !important;
    padding-bottom: 0.8rem !important;
    margin-bottom: 0 !important;
}}

h3, [data-testid="stHeadingWithActionElements"] h3, [data-testid="stHeading"] h3 {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_subtitulo"]} !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em !important;
    color: {estilo["color_subtitulo"]} !important;
    text-align: {estilo["alineacion_subtitulo"]} !important;
    width: 100% !important;
    padding-bottom: 0.2rem !important;
    margin-bottom: 0 !important;
}}

p, li {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_texto_general"]} !important;
    color: {estilo["color_texto_general"]} !important;
    margin-top: 5px !important;
    margin-bottom: 5px !important;
    letter-spacing: 0.02em !important;
    line-height: 1.6 !important;
}}

[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_etiqueta_caption"]} !important;
    margin-top: 2px !important;
    margin-bottom: 0px !important;
    line-height: 1.35 !important;
}}

/* Contenedores nativos de Streamlit convertidos en tarjetas Bento redondeadas */
div[data-testid="stVerticalBlockBorderWrapper"] {{
    background-color: {estilo["color_fondo_tarjetas"]} !important;
    border: 1px solid {estilo["color_borde_tarjetas"]} !important;
    border-radius: {estilo["radio_borde_tarjetas"]} !important;
    padding: 22px 26px !important;
    box-shadow: 0 4px 18px rgba(12, 35, 64, 0.04) !important;
    margin-bottom: 16px !important;
}}

/* Tarjetas Bento del Design System "Clinico limpio" */
.tarjeta-bento {{
    border-radius: {estilo["radio_borde_tarjetas"]};
    padding: 24px 26px;
    margin-bottom: 18px;
    box-shadow: 0 4px 16px rgba(12, 35, 64, 0.04);
    height: 100%;
}}

.tarjeta-blanca {{
    background-color: {estilo["color_fondo_tarjetas"]};
    border: 1px solid {estilo["color_borde_tarjetas"]};
    color: {estilo["color_tinta"]};
}}

.tarjeta-superficie {{
    background-color: {estilo["color_superficie_suave"]};
    border: 1px solid #C5D9EA;
    margin-top: 2rem;
    margin-bottom: 2rem;
    color: {estilo["color_tinta"]};
}}

.tarjeta-clinica {{
    background-color: {estilo["color_azul_clinico"]};
    color: #FFFFFF !important;
    border: none;
}}

.tarjeta-clinica h3, .tarjeta-clinica p, .tarjeta-clinica div, .tarjeta-clinica span {{
    color: #FFFFFF !important;
}}

.tarjeta-rosa-alerta {{
    background-color: {estilo["color_superficie_rosa"]};
    border: 1px solid #E5C5CF;
    color: {estilo["color_tinta"]};
}}

/* Compatibilidad con nombres previos de tarjetas */
.tarjeta-azul, .tarjeta-verde, .tarjeta-amarilla {{
    background-color: {estilo["color_superficie_suave"]};
    border: 1px solid #C5D9EA;
    color: {estilo["color_tinta"]};
}}

.tarjeta-rosa {{
    background-color: {estilo["color_superficie_rosa"]};
    border: 1px solid #E5C5CF;
    color: {estilo["color_tinta"]};
}}

.tarjeta-bosque {{
    background: linear-gradient(135deg, {estilo["color_tinta"]} 0%, {estilo["color_azul_clinico"]} 100%);
    color: #FFFFFF !important;
    border: none;
}}

.tarjeta-bosque h3, .tarjeta-bosque p, .tarjeta-bosque div, .tarjeta-bosque span {{
    color: #FFFFFF !important;
}}

.kpi-valor-grande {{
    font-size: 35px;
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 14px;
}}

.kpi-detalle-fila {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    align-items: center;
    font-size: 14px;
    font-weight: 500;
}}

/* Etiquetas tipo pildora (Badges) */
.pildora {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 18px;
    font-weight: 500;
    line-height: 1.4;
}}

.pildora-oscura {{
    background-color: {estilo["color_tinta"]};
    color: #FFFFFF !important;
}}

.pildora-clinica {{
    background-color: {estilo["color_azul_clinico"]};
    color: #FFFFFF !important;
}}

.pildora-blanca {{
    background-color: rgba(255, 255, 255, 0.9);
    color: {estilo["color_tinta"]} !important;
}}

.pildora-rosa {{
    background-color: {estilo["color_rosa_apagado"]};
    color: #FFFFFF !important;
}}

.pildora-suave, .pildora-azul, .pildora-verde, .pildora-amarilla {{
    background-color: {estilo["color_superficie_suave"]};
    color: {estilo["color_tinta"]} !important;
}}

.fila-item-bento {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 5px;
    padding: 7px 10px;
    border-radius: 14px;
    margin-bottom: 10px;
    background-color: {estilo["color_fondo_pagina"]};
    border: 1px solid {estilo["color_borde_tarjetas"]};
}}

/* Textos y distribucion horizontal de las tarjetas de Ruta Clinica */
.ruta-clinica-contenedor {{
    display: grid;
    grid-template-columns: {columnas_ruta_css};
    gap: 18px;
    align-items: stretch;
    margin-top: 10px;
    margin-bottom: 24px;
}}

.ruta-clinica-contenedor .tarjeta-bento {{
    margin-top: 0 !important;
    margin-bottom: 0 !important;
    height: 100%;
    padding: 20px 20px;
}}

@media (max-width: 1100px) {{
    .ruta-clinica-contenedor {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }}
}}

@media (max-width: 640px) {{
    .ruta-clinica-contenedor {{
        grid-template-columns: 1fr;
    }}
}}

.ruta-clinica-contenedor h3 {{
    font-size: {estilo["tamano_titulo_ruta_clinica"]} !important;
}}

.ruta-clinica-contenedor p,
.ruta-clinica-contenedor li,
.ruta-clinica-contenedor .fila-item-bento,
.ruta-clinica-contenedor .fila-item-bento div,
.ruta-clinica-contenedor code {{
    font-size: {estilo["tamano_texto_ruta_clinica"]} !important;
    line-height: 1.5 !important;
}}

/* Pildoras generales de Ruta Clinica (separadas de Cancer de Mama 2015 - 2024 y Alerta Sanitaria 2020) */
.ruta-clinica-contenedor .pildora {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_pildora_ruta_clinica"]} !important;
    font-weight: 500;
    line-height: 1.4;
    padding: 4px 12px;
    border-radius: 999px;
}}

/* Pildoras de las filas BI-RADS (Complementar, Normal / Benigno, Control 6 meses, Alerta GES / Biopsia, Confirmado) */
.ruta-clinica-contenedor .fila-item-bento .pildora {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_pildora_birads"]} !important;
    font-weight: 400;
    line-height: 1.4;
    padding: 2px 11px;
    border-radius: 999px;
    white-space: normal;
}}

/* Tipografia monoespaciada IBM Plex Mono para todo el codigo */
[data-testid="stCode"] pre, code, pre, code span {{
    font-family: {estilo["familia_fuente_mono"]} !important;
    font-size: {estilo["tamano_codigo"]} !important;
}}

[data-testid="stCode"] {{
    border-radius: 24px !important;
    overflow: hidden !important;
    border: 1px solid {estilo["color_borde_tarjetas"]} !important;
}}

.contenedor-tabla-rem {{
    max-height: {estilo["altura_maxima_tabla"]} !important;
    overflow-y: auto !important;
    overflow-x: auto !important;
    margin-top: 10px;
    margin-bottom: 20px;
    background-color: {estilo["color_fondo_tarjetas"]};
    border: 1px solid {estilo["color_borde_tarjetas"]};
    border-radius: 24px;
}}

.contenedor-tabla-esquema {{
    width: {estilo["ancho_tabla_esquema"]} !important;
    max-height: {estilo["altura_maxima_tabla_esquema"]} !important;
    overflow-y: auto !important;
    overflow-x: auto !important;
    margin-top: 5px;
    margin-bottom: 20px;
    background-color: {estilo["color_fondo_tarjetas"]};
    border: 1px solid {estilo["color_borde_tarjetas"]};
    border-radius: 24px;
}}

.contenedor-tabla-consolidacion {{
    width: {estilo["ancho_tabla_consolidacion"]} !important;
    max-width: 100% !important;
    max-height: {estilo["altura_maxima_tabla_consolidacion"]} !important;
    overflow-y: auto !important;
    overflow-x: auto !important;
    margin-top: 8px;
    margin-bottom: 20px;
    background-color: {estilo["color_fondo_tarjetas"]};
    border: 1px solid {estilo["color_borde_tarjetas"]};
    border-radius: 16px;
}}

.tabla-rem-estilizada,
.tabla-rem-estilizada th,
.tabla-rem-estilizada td {{
    font-family: {estilo["familia_fuente"]} !important;
    font-size: {estilo["tamano_letra_tabla"]} !important;
    color: {estilo["color_texto_general"]} !important;
}}

.tabla-rem-estilizada {{
    width: 100%;
    margin: 0 !important;
    border-collapse: collapse !important;
    border: none !important;
}}

.tabla-esquema-estilizada,
.tabla-esquema-estilizada th,
.tabla-esquema-estilizada td {{
    font-size: {estilo["tamano_letra_tabla_esquema"]} !important;
}}

.tabla-rem-estilizada thead tr,
.tabla-rem-estilizada tbody tr {{
    border: none !important;
}}

.tabla-rem-estilizada thead th {{
    position: sticky;
    top: 0;
    z-index: 2;
    background-color: {estilo["color_fondo_encabezado_tabla"]};
    color: {estilo["color_texto_encabezado_tabla"]} !important;
    font-weight: 500;
    text-align: left;
    padding: 8px 12px;
    border-top: none !important;
    border-bottom: 2px solid #C5D9EA !important;
}}

.tabla-rem-estilizada tbody td {{
    padding: {estilo["relleno_fila_tabla"]} !important;
    border-top: none !important;
    border-bottom: 1px solid {estilo["color_borde_tarjetas"]} !important;
}}

.tabla-esquema-estilizada thead th,
.tabla-esquema-estilizada tbody td {{
    padding: {estilo["relleno_fila_tabla_esquema"]} !important;
    line-height: 1.25 !important;
}}

.tabla-consolidacion-estilizada,
.tabla-consolidacion-estilizada th,
.tabla-consolidacion-estilizada td {{
    font-size: {estilo["tamano_letra_tabla_consolidacion"]} !important;
}}

.tabla-consolidacion-estilizada thead th,
.tabla-consolidacion-estilizada tbody td {{
    padding: {estilo["relleno_fila_tabla_consolidacion"]} !important;
    line-height: 1.2 !important;
}}

.tabla-consolidacion-estilizada thead th:first-child,
.tabla-consolidacion-estilizada tbody td:first-child {{
    padding-left: 10px !important;
}}

.tabla-consolidacion-estilizada thead th:last-child,
.tabla-consolidacion-estilizada tbody td:last-child {{
    padding-right: 10px !important;
}}

.tabla-rem-estilizada thead th:first-child,
.tabla-rem-estilizada tbody td:first-child {{
    border-left: none !important;
}}

.tabla-rem-estilizada thead th:last-child,
.tabla-rem-estilizada tbody td:last-child {{
    border-right: none !important;
}}

.tabla-rem-estilizada tbody tr:last-child td {{
    border-bottom: none !important;
}}

.tabla-rem-estilizada tbody tr:hover {{
    background-color: {estilo["color_fondo_pagina"]};
}}
</style>"""
    st.markdown(bloque_css, unsafe_allow_html=True)
