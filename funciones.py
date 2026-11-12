import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from estilos import CONFIGURACION_ESTILO


# ==============================================================================
# FUNCIONES PLANTILLA PARA AGREGAR NUEVOS BLOQUES Y TARJETAS BENTO AL DASHBOARD
# ==============================================================================

def mostrar_tarjeta_kpi_bento(
    titulo_kpi,
    valor_principal,
    texto_etiqueta="",
    detalle_secundario="",
    color_tarjeta="superficie",
):
    """
    Renderiza una tarjeta de indicador (KPI) siguiendo el Design System
    'Clinico limpio':
    - 'clinica': fondo azul clinico / tinta con texto blanco
    - 'superficie': fondo superficie suave (#DBE8F3) con texto tinta (#0C2340)
    - 'rosa_alerta': acento rosa apagado reservado para alertas de cancer de mama
    - 'blanca': tarjeta blanca limpia con borde suave
    """
    clases_validas = {
        "clinica": "tarjeta-clinica",
        "superficie": "tarjeta-superficie",
        "rosa_alerta": "tarjeta-rosa-alerta",
        "blanca": "tarjeta-blanca",
        "amarilla": "tarjeta-superficie",
        "verde": "tarjeta-superficie",
        "azul": "tarjeta-superficie",
        "rosa": "tarjeta-rosa-alerta",
        "bosque": "tarjeta-clinica",
    }
    clase_color = clases_validas.get(color_tarjeta, "tarjeta-blanca")

    if color_tarjeta in ("rosa_alerta", "rosa"):
        clase_pildora = "pildora-rosa"
    elif color_tarjeta in ("clinica", "bosque"):
        clase_pildora = "pildora-blanca"
    elif color_tarjeta == "blanca":
        clase_pildora = "pildora-suave"
    else:
        clase_pildora = "pildora-clinica"

    bloque_detalle = ""
    if texto_etiqueta or detalle_secundario:
        html_pildora = (
            f'<span class="pildora {clase_pildora}">{texto_etiqueta}</span>'
            if texto_etiqueta
            else ""
        )
        html_texto = f"<span>{detalle_secundario}</span>" if detalle_secundario else ""
        bloque_detalle = f'<div class="kpi-detalle-fila">{html_pildora}{html_texto}</div>'

    html_tarjeta = f"""
    <div class="tarjeta-bento {clase_color}">
        <div class="kpi-valor-grande" style="margin-bottom: 0;">{valor_principal}</div>
        {bloque_detalle}
    </div>
    """
    st.markdown(html_tarjeta, unsafe_allow_html=True)


def mostrar_tabla_configurable(tabla_resultado, es_tabla_esquema=None, tipo_tabla=None):
    """
    Renderiza un DataFrame diferenciando entre las tablas de esquema, la tabla
    de consolidacion historica y las tablas generales de ejemplos resultantes.
    """
    estilo = CONFIGURACION_ESTILO
    if es_tabla_esquema is None:
        columnas_actuales = set(tabla_resultado.columns)
        es_tabla_esquema = {"columna", "descripcion"}.issubset(columnas_actuales)

    if estilo.get("usar_tabla_html_escalable", True):
        if tipo_tabla == "consolidacion":
            clases_tabla = "tabla-rem-estilizada tabla-consolidacion-estilizada"
            clase_contenedor = "contenedor-tabla-consolidacion"
        elif es_tabla_esquema:
            clases_tabla = "tabla-rem-estilizada tabla-esquema-estilizada"
            clase_contenedor = "contenedor-tabla-esquema"
        else:
            clases_tabla = "tabla-rem-estilizada"
            clase_contenedor = "contenedor-tabla-rem"
        html_tabla = tabla_resultado.to_html(
            index=False, classes=clases_tabla, border=0
        )
        st.markdown(
            f'<div class="{clase_contenedor}">{html_tabla}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.dataframe(tabla_resultado, width="stretch", hide_index=True)


def mostrar_bloque_codigo_y_tabla(
    titulo_bloque,
    descripcion_bloque,
    codigo_ejemplo,
    tabla_resultado,
    lenguaje_codigo="python",
    en_columnas=True,
    explicacion_inferior=None,
):
    """
    Plantilla reutilizable para mostrar un ejemplo de codigo junto con la tabla
    que produce como resultado dentro de una tarjeta Bento redondeada.
    """
    estilo = CONFIGURACION_ESTILO
    proporciones = estilo.get("proporcion_columnas_codigo_tabla", [0.65, 1.75])

    with st.container(border=False):
        if titulo_bloque:
            st.subheader(titulo_bloque)
        if descripcion_bloque:
            st.markdown(descripcion_bloque)

        if en_columnas:
            columna_codigo, columna_tabla = st.columns(proporciones, gap="small")
            with columna_codigo:
                st.caption("Ejemplo código de consulta")
                st.code(codigo_ejemplo, language=lenguaje_codigo)
            with columna_tabla:
                st.caption("Vista de la tabla resultante")
                mostrar_tabla_configurable(tabla_resultado)
        else:
            st.caption("Código de consulta")
            st.code(codigo_ejemplo, language=lenguaje_codigo)
            st.caption("Vista de la tabla resultante")
            mostrar_tabla_configurable(tabla_resultado)

        if explicacion_inferior:
            st.info(explicacion_inferior)


def mostrar_bloque_grafico(
    titulo_grafico,
    descripcion_previa,
    figura_plotly,
    comentario_hallazgo=None,
):
    """
    Plantilla reutilizable para presentar un grafico interactivo de Plotly
    dentro de una tarjeta Bento redondeada junto con su contexto clinico.
    """
    with st.container(border=False):
        st.subheader(titulo_grafico)
        st.markdown(descripcion_previa)
        st.plotly_chart(figura_plotly, width="stretch")
        if comentario_hallazgo:
            st.markdown(comentario_hallazgo)


# ==============================================================================
# DATOS PRE-CARGADOS DE EJEMPLO (TABLAS Y CATALOGO DEIS-REM)
# ==============================================================================

def obtener_esquema_hechos():
    return pd.DataFrame([
        {
            "columna": "year",
            "tipo_dato": "bigint",
            "descripcion": "Año del registro",
        },
        {
            "columna": "mes",
            "tipo_dato": "tinyint",
            "descripcion": "Mes del conteo reportado (de enero a diciembre)",
        },
        {
            "columna": "tipo_serie",
            "tipo_dato": "string",
            "descripcion": "Serie REM a la que pertenece la hoja: a, bs, bm, d o p",
        },
        {
            "columna": "id_establecimiento",
            "tipo_dato": "string",
            "descripcion": "Identificador oficial DEIS del establecimiento de salud",
        },
        {
            "columna": "cod_prestacion",
            "tipo_dato": "string",
            "descripcion": "Código de la prestación o actividad clínica registrada",
        },
        {
            "columna": "cod_col_numerica",
            "tipo_dato": "string",
            "descripcion": "Código de la columna numérica dentro de la hoja (ej: col01 para total)",
        },
        {
            "columna": "cantidad",
            "tipo_dato": "double",
            "descripcion": "Valor numérico reportado para el establecimiento, prestación y columna",
        },
    ])


def obtener_esquema_codigos():
    return pd.DataFrame([
        {
            "columna": "year",
            "tipo_dato": "bigint",
            "descripcion": "Año de vigencia del diccionario REM",
        },
        {
            "columna": "tipo_serie",
            "tipo_dato": "string",
            "descripcion": "Serie REM a la que pertenece la hoja: a, bs, bm, d o p",
        },
        {
            "columna": "cod_hoja",
            "tipo_dato": "string",
            "descripcion": "Código identificador de la hoja REM (ej: a04, a29, b, bm18a)",
        },
        {
            "columna": "nombre_hoja",
            "tipo_dato": "string",
            "descripcion": "Nombre descriptivo de la hoja clínica",
        },
        {
            "columna": "nombre_seccion",
            "tipo_dato": "string",
            "descripcion": "Nombre de la sección clínica dentro de la hoja",
        },
        {
            "columna": "cod_prestacion",
            "tipo_dato": "string",
            "descripcion": "Código de la prestación (llave para cruzar con la tabla hechos)",
        },
        {
            "columna": "nombre_prestacion",
            "tipo_dato": "string",
            "descripcion": "Glosa clínica descriptiva de la fila o actividad registrada",
        },
        {
            "columna": "cod_col_numerica",
            "tipo_dato": "string",
            "descripcion": "Código de la columna numérica (col01, col02, etc., llave para cruzar con hechos)",
        },
        {
            "columna": "nombre_col_numerica",
            "tipo_dato": "string",
            "descripcion": "Descripción de lo que mide esa columna (ej: total ambos sexos, sexo o tramo etario)",
        },
    ])


def obtener_muestra_hechos():
    return pd.DataFrame([
        {"year": 2024, "mes": 1, "tipo_serie": "a", "id_establecimiento": "101010", "cod_prestacion": "06020201", "cod_col_numerica": "col01", "cantidad": 22.0, "categoria": "salud", "fuente": "deis", "pais": "cl"},
        {"year": 2024, "mes": 1, "tipo_serie": "a", "id_establecimiento": "101010", "cod_prestacion": "06020201", "cod_col_numerica": "col02", "cantidad": 21.0, "categoria": "salud", "fuente": "deis", "pais": "cl"},
        {"year": 2024, "mes": 1, "tipo_serie": "a", "id_establecimiento": "101010", "cod_prestacion": "06020201", "cod_col_numerica": "col03", "cantidad": 1.0, "categoria": "salud", "fuente": "deis", "pais": "cl"},
        {"year": 2024, "mes": 1, "tipo_serie": "a", "id_establecimiento": "101010", "cod_prestacion": "06020201", "cod_col_numerica": "col12", "cantidad": 4.0, "categoria": "salud", "fuente": "deis", "pais": "cl"},
    ])


def obtener_muestra_codigos():
    return pd.DataFrame([
        {
            "year": 2024,
            "cod_hoja": "a04",
            "nombre_hoja": "consultas y otras atenciones en la red",
            "nombre_seccion": "consultas medicas",
            "nombre_prestacion": "tipo de atencion| salud mental",
            "cod_prestacion": "04025025",
            "cod_col_numerica": "col01",
            "nombre_col_numerica": "tipo de conteo| total; sexo| ambos sexos",
        },
        {
            "year": 2024,
            "cod_hoja": "a04",
            "nombre_hoja": "consultas y otras atenciones en la red",
            "nombre_seccion": "consultas medicas",
            "nombre_prestacion": "tipo de atencion| salud mental",
            "cod_prestacion": "04025025",
            "cod_col_numerica": "col02",
            "nombre_col_numerica": "tipo de conteo| total; sexo| hombres",
        },
        {
            "year": 2024,
            "cod_hoja": "a04",
            "nombre_hoja": "consultas y otras atenciones en la red",
            "nombre_seccion": "consultas medicas",
            "nombre_prestacion": "tipo de atencion| salud mental",
            "cod_prestacion": "04025025",
            "cod_col_numerica": "col03",
            "nombre_col_numerica": "tipo de conteo| total; sexo| mujeres",
        },
        {
            "year": 2024,
            "cod_hoja": "a04",
            "nombre_hoja": "consultas y otras atenciones en la red",
            "nombre_seccion": "consultas medicas",
            "nombre_prestacion": "tipo de atencion| salud mental",
            "cod_prestacion": "04025025",
            "cod_col_numerica": "col04",
            "nombre_col_numerica": "edad| menor de 1 anio; sexo| hombres",
        },
    ])


def obtener_esquema_jerarquia_prestaciones():
    return pd.DataFrame([
        {
            "columna": "num_prestacion",
            "tipo_dato": "int",
            "descripcion": "Clave numérica del nodo en el árbol de glosas de las prestaciones (cruza con códigos)",
        },
        {
            "columna": "clave",
            "tipo_dato": "string",
            "descripcion": "Parte clave del par clave|valor de este nivel de la glosa (ej: actividad, tipo de examen)",
        },
        {
            "columna": "valor",
            "tipo_dato": "string",
            "descripcion": "Parte valor del par clave|valor de este nivel de la glosa, sin la unidad",
        },
        {
            "columna": "nivel",
            "tipo_dato": "bigint",
            "descripcion": "Profundidad del nodo en el árbol jerárquico de glosas, comenzando desde 1",
        },
        {
            "columna": "num_prestacion_padre",
            "tipo_dato": "int",
            "descripcion": "Clave del nodo padre en el mismo árbol (es nulo cuando el nodo está en la raíz)",
        },
        {
            "columna": "unidad",
            "tipo_dato": "string",
            "descripcion": "Unidad extraída del valor (meses o años); es nula cuando la glosa no la indica",
        },
    ])


def obtener_muestra_jerarquia_prestaciones():
    return pd.DataFrame([
        {"num_prestacion": 1, "clave": "actividad", "valor": "65 y mas", "nivel": 1, "num_prestacion_padre": None, "unidad": None},
        {"num_prestacion": 2, "clave": "actividad", "valor": "a colegio, salas cuna, jardin infantil", "nivel": 1, "num_prestacion_padre": None, "unidad": None},
        {"num_prestacion": 3, "clave": "actividad", "valor": "a grupo comunitario", "nivel": 1, "num_prestacion_padre": None, "unidad": None},
        {"num_prestacion": 4, "clave": "actividad", "valor": "a institucion (eleam, carceles, colegios, sala cuna)", "nivel": 1, "num_prestacion_padre": None, "unidad": None},
    ])


def obtener_esquema_jerarquia_columnas():
    return pd.DataFrame([
        {
            "columna": "num_col_numerica",
            "tipo_dato": "int",
            "descripcion": "Clave numérica del nodo en el árbol de glosas de las columnas numéricas (cruza con códigos)",
        },
        {
            "columna": "clave",
            "tipo_dato": "string",
            "descripcion": "Parte clave del par clave|valor de este nivel de la columna (ej: sexo, edad, tipo de conteo)",
        },
        {
            "columna": "valor",
            "tipo_dato": "string",
            "descripcion": "Parte valor del par clave|valor de este nivel de la columna, sin la unidad",
        },
        {
            "columna": "nivel",
            "tipo_dato": "bigint",
            "descripcion": "Profundidad del nodo en el árbol de glosas de columnas, comenzando desde 1",
        },
        {
            "columna": "num_col_numerica_padre",
            "tipo_dato": "int",
            "descripcion": "Clave del nodo padre en el mismo árbol (es nulo en la raíz)",
        },
        {
            "columna": "unidad",
            "tipo_dato": "string",
            "descripcion": "Unidad extraída del valor; es nula cuando la glosa no indica unidad",
        },
    ])


def obtener_muestra_jerarquia_columnas():
    return pd.DataFrame([
        {"num_col_numerica": 1, "clave": "acompanante", "valor": "madre, padre o cuidador", "nivel": 1, "num_col_numerica_padre": None, "unidad": None},
        {"num_col_numerica": 2, "clave": "agresor/a", "valor": "conocido/a", "nivel": 1, "num_col_numerica_padre": None, "unidad": None},
        {"num_col_numerica": 3, "clave": "agresor/a", "valor": "desconocido/a", "nivel": 1, "num_col_numerica_padre": None, "unidad": None},
        {"num_col_numerica": 4, "clave": "agresor/a", "valor": "familiar", "nivel": 1, "num_col_numerica_padre": None, "unidad": None},
    ])


def obtener_esquema_establecimientos():
    return pd.DataFrame([
        {
            "columna": "id_establecimiento",
            "tipo_dato": "string",
            "descripcion": "Código vigente del establecimiento de salud asignado por DEIS (único en esta tabla)",
        },
        {
            "columna": "year_ultimo_cambio",
            "tipo_dato": "int",
            "descripcion": "Año de la edición anual más reciente del registro de establecimientos de la que provienen los datos",
        },
        {
            "columna": "nombre_establecimiento",
            "tipo_dato": "string",
            "descripcion": "Nombre oficial del establecimiento normalizado en minúsculas y sin tildes",
        },
        {
            "columna": "tipo_establecimiento",
            "tipo_dato": "string",
            "descripcion": "Tipo de establecimiento (ej: hospital, centro de salud familiar, posta de salud rural)",
        },
        {
            "columna": "dependencia_admin",
            "tipo_dato": "string",
            "descripcion": "Entidad de la que depende administrativamente (ej: municipal, servicio de salud, privado)",
        },
        {
            "columna": "nivel_atencion",
            "tipo_dato": "string",
            "descripcion": "Nivel de atención del establecimiento: primario, secundario o terciario",
        },
        {
            "columna": "nivel_complejidad",
            "tipo_dato": "string",
            "descripcion": "Nivel de complejidad: baja, mediana, alta o no aplica",
        },
        {
            "columna": "nombre_region",
            "tipo_dato": "string",
            "descripcion": "Nombre de la región en que se ubica el establecimiento",
        },
        {
            "columna": "nombre_comuna",
            "tipo_dato": "string",
            "descripcion": "Nombre de la comuna en que se ubica el establecimiento",
        },
        {
            "columna": "cod_comuna",
            "tipo_dato": "string",
            "descripcion": "Código oficial de la comuna (CUT) de cinco dígitos actualizado",
        },
        {
            "columna": "nombre_servicio_salud",
            "tipo_dato": "string",
            "descripcion": "Nombre del Servicio de Salud al que pertenece el establecimiento",
        },
    ])


def obtener_muestra_establecimientos():
    return pd.DataFrame([
        {
            "id_establecimiento": "101010",
            "nombre_establecimiento": "actividades gestionadas por la direccion del servicio para apoyo de la red",
            "tipo_establecimiento": "otro",
            "dependencia_admin": "servicio de salud",
            "nivel_complejidad": "baja",
            "nombre_region": "arica y parinacota",
            "nombre_comuna": "arica",
            "nombre_servicio_salud": "servicio de salud arica y parinacota",
        },
        {
            "id_establecimiento": "101011",
            "nombre_establecimiento": "prais",
            "tipo_establecimiento": "otro",
            "dependencia_admin": "servicio de salud",
            "nivel_complejidad": "baja",
            "nombre_region": "arica y parinacota",
            "nombre_comuna": "arica",
            "nombre_servicio_salud": "servicio de salud arica y parinacota",
        },
        {
            "id_establecimiento": "101012",
            "nombre_establecimiento": "clinica dental movil simple. pat. pw4076",
            "tipo_establecimiento": "unidad de procedimientos movil",
            "dependencia_admin": "servicio de salud",
            "nivel_complejidad": "baja",
            "nombre_region": "arica y parinacota",
            "nombre_comuna": "arica",
            "nombre_servicio_salud": "servicio de salud arica y parinacota",
        },
        {
            "id_establecimiento": "101030",
            "nombre_establecimiento": "unidad de salud funcionario s.s arica",
            "tipo_establecimiento": "otro",
            "dependencia_admin": "servicio de salud",
            "nivel_complejidad": "baja",
            "nombre_region": "arica y parinacota",
            "nombre_comuna": "arica",
            "nombre_servicio_salud": "servicio de salud arica y parinacota",
        },
    ])


def obtener_esquema_establecimientos_historial():
    return pd.DataFrame([
        {
            "columna": "id_establecimiento",
            "tipo_dato": "string",
            "descripcion": "Código vigente del establecimiento al que corresponde el valor histórico (cruza con establecimientos)",
        },
        {
            "columna": "nombre_columna",
            "tipo_dato": "string",
            "descripcion": "Nombre del atributo de la tabla de establecimientos que cambió, o id_establecimiento_antiguo",
        },
        {
            "columna": "valor_columna",
            "tipo_dato": "string",
            "descripcion": "Valor anterior que tuvo el atributo (o código antiguo del establecimiento), guardado como texto",
        },
        {
            "columna": "tipo_columna",
            "tipo_dato": "string",
            "descripcion": "Tipo de dato original antes de guardarlo como texto (String, Date, Float64 o Boolean)",
        },
        {
            "columna": "year_inicio",
            "tipo_dato": "int",
            "descripcion": "Primer año en que el atributo tuvo este valor en el registro oficial",
        },
        {
            "columna": "year_termino",
            "tipo_dato": "int",
            "descripcion": "Último año en que el atributo tuvo este valor en el registro oficial",
        },
    ])


def obtener_muestra_establecimientos_historial():
    return pd.DataFrame([
        {"id_establecimiento": "101010", "nombre_columna": "id_establecimiento_antiguo", "valor_columna": "01-010", "tipo_columna": "String", "year_inicio": 2014, "year_termino": 2026},
        {"id_establecimiento": "101010", "nombre_columna": "tipo_establecimiento", "valor_columna": "direccion servicio de salud", "tipo_columna": "String", "year_inicio": 2014, "year_termino": 2024},
        {"id_establecimiento": "101010", "nombre_columna": "condicion", "valor_columna": "vigente en operacion", "tipo_columna": "String", "year_inicio": 2014, "year_termino": 2023},
        {"id_establecimiento": "101010", "nombre_columna": "fecha_apertura", "valor_columna": "2009-01-01", "tipo_columna": "Date", "year_inicio": 2014, "year_termino": 2022},
    ])


def obtener_muestra_busqueda_mama():
    return pd.DataFrame([
        {
            "cod_hoja": "a07",
            "nombre_hoja": "atencion de especialidades",
            "nombre_seccion": "atenciones medicas por programas y policlinicos (incluidas en seccion a)",
            "coincidencias": 2,
            "ejemplo": "atencion| cirugia de mamas",
        },
        {
            "cod_hoja": "a24",
            "nombre_hoja": "atencion obstetrica y del recien nacido",
            "nombre_seccion": "egresos de maternidad y neonatologia, segun lactancia materna exclusiva",
            "coincidencias": 1,
            "ejemplo": "tipo de alimentacion| egresados con madres acogidas a la ley 21.155 (derecho a no amamantar)",
        },
        {
            "cod_hoja": "a29",
            "nombre_hoja": "programa de imagenes diagnosticas y/o resolutividad en atencion primaria",
            "nombre_seccion": "procedimientos de imagenes diagnosticas y programa de resolutividad en aps",
            "coincidencias": 3,
            "ejemplo": "tipo de examen| ecotomografia mamaria; estado| informadas",
        },
        {
            "cod_hoja": "b",
            "nombre_hoja": "sin clasificacion de hoja",
            "nombre_seccion": "cirugia plastica y reparadora",
            "coincidencias": 1,
            "ejemplo": "prestacion| reconstruccion mamaria",
        },
        {
            "cod_hoja": "b",
            "nombre_hoja": "sin clasificacion de hoja",
            "nombre_seccion": "imagenologia",
            "coincidencias": 6,
            "ejemplo": "prestacion| biopsia mamaria guiada por ecotomografia",
        },
        {
            "cod_hoja": "b",
            "nombre_hoja": "sin clasificacion de hoja",
            "nombre_seccion": "medicina nuclear y radioterapia",
            "coincidencias": 1,
            "ejemplo": "tipo de estudio| estudios oncologicos; prestacion| estudio glandulas mamarias (mamocintigrafia)",
        },
        {
            "cod_hoja": "b",
            "nombre_hoja": "sin clasificacion de hoja",
            "nombre_seccion": "intervenciones quirurgicas",
            "coincidencias": 6,
            "ejemplo": "prestacion| absceso y/o hematoma de mama, tratamiento quirurgico",
        },
        {
            "cod_hoja": "b17",
            "nombre_hoja": "actividades de apoyo diagnostico y terapeutico",
            "nombre_seccion": "intervenciones quirurgicas",
            "coincidencias": 1,
            "ejemplo": "intervencion quirurgica por especialidad| cirugia de la mama",
        },
        {
            "cod_hoja": "bm18a",
            "nombre_hoja": "libro de prestaciones de apoyo diagnostico y terapeutico (establecimientos municipales)",
            "nombre_seccion": "examenes de diagnostico",
            "coincidencias": 3,
            "ejemplo": "examen| ecografia mamaria bilateral (incluye doppler)",
        },
        {
            "cod_hoja": "p12",
            "nombre_hoja": "personas con tamizaje para la deteccion precoz de cancer de cuello uterino - mamografia",
            "nombre_seccion": "programa de cancer de cuello uterino y patologia mamaria",
            "coincidencias": 26,
            "ejemplo": "poblacion| 25-29 anios",
        },
    ])


def obtener_muestra_codigos_antiguos_mamografia():
    return pd.DataFrame([
        {"cod_hoja": "bm18", "cod_prestacion": "18090500", "nombre_prestacion": "glosa| mamografía; estado| solicitadas", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18090600", "nombre_prestacion": "glosa| mamografía; estado| informadas", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18090700", "nombre_prestacion": "glosa| mamografía; evaluación| con birads 0", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18090800", "nombre_prestacion": "glosa| mamografía; evaluación| con birads 1 o 2", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18090990", "nombre_prestacion": "glosa| mamografía; estado| con birads 3", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18200100", "nombre_prestacion": "glosa| mamografía; estado| con birads 4, 5 o 6", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18", "cod_prestacion": "18200200", "nombre_prestacion": "glosa| mamografía; estado| sin informe birads", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bm18a", "cod_prestacion": "80401010", "nombre_prestacion": "examen| mamografía bilateral (4 exp.)", "anio_inicio": 2015, "anio_termino": 2025},
        {"cod_hoja": "bm18a", "cod_prestacion": "80401110", "nombre_prestacion": "examen| mamografía unilateral (2 exp.)", "anio_inicio": 2015, "anio_termino": 2025},
        {"cod_hoja": "bs17", "cod_prestacion": "17150100", "nombre_prestacion": "glosa| mamografía; estado| solicitadas", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150200", "nombre_prestacion": "glosa| mamografía; estado| informadas", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150300", "nombre_prestacion": "glosa| mamografía; estado| con birads 0", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150400", "nombre_prestacion": "glosa| mamografía; estado| con birads 1 o 2", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150500", "nombre_prestacion": "glosa| mamografía; estado| con birads 3", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150600", "nombre_prestacion": "glosa| mamografía; estado| con birads 4, 5 o 6", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17", "cod_prestacion": "17150700", "nombre_prestacion": "glosa| mamografía; estado| sin informe birads", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17a", "cod_prestacion": "17a0401010", "nombre_prestacion": "prestacion| mamografía bilateral (4 exposiciones)", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17a", "cod_prestacion": "17a0401110", "nombre_prestacion": "prestacion| mamografía unilateral (2 exposiciones)", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17d", "cod_prestacion": "17d0401010", "nombre_prestacion": "glosa| mamografía bilateral (4 exp.)", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17d", "cod_prestacion": "17d0401110", "nombre_prestacion": "glosa| mamografía unilateral (2 exp.)", "anio_inicio": 2015, "anio_termino": 2016},
        {"cod_hoja": "bs17a", "cod_prestacion": "17a0401130", "nombre_prestacion": "prestacion| mamografía proyección complementaria (axilar, magnificada, compresión focalizada)", "anio_inicio": 2016, "anio_termino": 2016},
        {"cod_hoja": "a29", "cod_prestacion": "29000007", "nombre_prestacion": "tipo de examen| mamografía; estado| solicitadas", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000008", "nombre_prestacion": "tipo de examen| mamografía; estado| informadas", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000009", "nombre_prestacion": "tipo de examen| mamografía; evaluación| con birads 0", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000010", "nombre_prestacion": "tipo de examen| mamografía; evaluación| con birads 1 o 2", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000011", "nombre_prestacion": "tipo de examen| mamografía; evaluación| con birads 3", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000012", "nombre_prestacion": "tipo de examen| mamografía; evaluación| con birads 4, 5 o 6", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000013", "nombre_prestacion": "tipo de examen| mamografía; evaluación| sin informe birads", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01010592", "nombre_prestacion": "prestacion| mamografía bilateral", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01010593", "nombre_prestacion": "prestacion| mamografía unilateral", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01010594", "nombre_prestacion": "prestacion| mamografía proyección complementaria (axilar, magnificada, compresión focalizada)", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01010779", "nombre_prestacion": "prestacion| marcación de microcalcificaciones mamarias bajo visión estereotáxica o ecográfica", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "bm18a", "cod_prestacion": "80401130", "nombre_prestacion": "examen| mamografía proyección complementaria (axilar, magnificada, compresión focalizada)", "anio_inicio": 2017, "anio_termino": 2025},
        {"cod_hoja": "a29", "cod_prestacion": "29000048", "nombre_prestacion": "tipo de examen| mamografía; proyección| magnificada o compresión focalizada", "anio_inicio": 2018, "anio_termino": 2025},
        {"cod_hoja": "a30", "cod_prestacion": "30000070", "nombre_prestacion": "teleinforme| número de mamografías", "anio_inicio": 2018, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01014145", "nombre_prestacion": "prestacion| mamografía bilateral digital 3d con tomosíntesis", "anio_inicio": 2020, "anio_termino": 2025},
        {"cod_hoja": "b", "cod_prestacion": "01014146", "nombre_prestacion": "prestacion| mamografía unilateral digital 3d con tomosíntesis", "anio_inicio": 2020, "anio_termino": 2025},
        {"cod_hoja": "a30ar", "cod_prestacion": "30100190", "nombre_prestacion": "teleinforme| número de teleinformes de mamografía", "anio_inicio": 2021, "anio_termino": 2025},
    ])


def obtener_resumen_hojas_mamografia():
    return pd.DataFrame([
        {
            "hoja_rem": "bm18 / bs17",
            "periodo_vigencia": "2015 - 2016",
            "nivel_atencion": "Atención Primaria (APS) y SS",
            "codigos_principales": "18090600, 17150200 (informadas), 18090800 / 17150400 (BIRADS 1-2), 18200100 / 17150600 (BIRADS 4-5-6)",
            "funcion_en_registro": "Registran mamografías del programa de imágenes en APS (municipales en bm18 y Servicios de Salud en bs17) antes de fusionarse en a29.",
        },
        {
            "hoja_rem": "bs17a / bs17d / bm18a",
            "periodo_vigencia": "2015 - 2025 (bm18a)",
            "nivel_atencion": "Hospitalario y Municipal",
            "codigos_principales": "17a0401010, 17d0401010, 80401010 (bilateral), 80401110 (unilateral)",
            "funcion_en_registro": "Contienen exámenes y cirugías realizadas en especialidad hospitalaria (bs17a/bs17d en 2015-2016) y compras desde establecimientos municipales (bm18a).",
        },
        {
            "hoja_rem": "a29",
            "periodo_vigencia": "2017 - 2025",
            "nivel_atencion": "Atención Primaria (APS)",
            "codigos_principales": "29000007 (solicitadas), 29000008 (informadas), 29000010 (BIRADS 1-2), 29000012 (BIRADS 4-5-6)",
            "funcion_en_registro": "Reemplaza a bm18 y bs17 para consolidar el Programa de Imágenes Diagnósticas en APS y su clasificación BI-RADS.",
        },
        {
            "hoja_rem": "b",
            "periodo_vigencia": "2017 - 2025",
            "nivel_atencion": "Hospitalario y Especialidad",
            "codigos_principales": "01010592 / 01014145 (bilateral 2D y 3D), 01012162 (mastectomía parcial), 01012163 (mastectomía radical)",
            "funcion_en_registro": "Centraliza imágenes hospitalarias (incluyendo tomosíntesis 3D desde 2020), biopsias y cirugías oncológicas mamarias.",
        },
        {
            "hoja_rem": "p12",
            "periodo_vigencia": "2015 - 2025",
            "nivel_atencion": "Población bajo control APS",
            "codigos_principales": "Cortes semestrales por grupo etario",
            "funcion_en_registro": "Registra la cobertura de mujeres con mamografía vigente y examen físico de mama al día.",
        },
    ])


# ==============================================================================
# CARGA Y PREPARACION DE DATOS DEL CASO DE ESTUDIO (CANCER DE MAMA)
# ==============================================================================

@st.cache_data
def cargar_datos_cancer_mama():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    rutas_candidatas = [
        os.path.join(directorio_actual, "datos_analisis_mama_2015_2025.parquet"),
        os.path.join(directorio_actual, "..", "datos_analisis_mama_2015_2025.parquet"),
        "datos_analisis_mama_2015_2025.parquet",
        "../datos_analisis_mama_2015_2025.parquet",
        "G:/Mi unidad/do/datopia/deis-rem/datos_analisis_mama_2015_2025.parquet",
    ]

    ruta_encontrada = None
    for ruta_posible in rutas_candidatas:
        if os.path.exists(ruta_posible):
            ruta_encontrada = ruta_posible
            break

    mapa_columnas_limpias = {
        "18090600": "mamografia_informada_aps",
        "17150200": "mamografia_informada_aps",
        "29000008": "mamografia_informada_aps",
        "18090700": "mamografia_birads_0",
        "17150300": "mamografia_birads_0",
        "29000009": "mamografia_birads_0",
        "18090800": "mamografia_birads_1_2",
        "17150400": "mamografia_birads_1_2",
        "29000010": "mamografia_birads_1_2",
        "18090990": "mamografia_birads_3",
        "17150500": "mamografia_birads_3",
        "29000011": "mamografia_birads_3",
        "18200100": "mamografia_birads_4_5_6",
        "17150600": "mamografia_birads_4_5_6",
        "29000012": "mamografia_birads_4_5_6",
        "17a0401010": "mamografia_bilateral_hospital",
        "17d0401010": "mamografia_bilateral_hospital",
        "1010592": "mamografia_bilateral_hospital",
        "1014145": "mamografia_bilateral_hospital",
        "80401010": "mamografia_bilateral_hospital",
        "17a0401110": "mamografia_unilateral_hospital",
        "17d0401110": "mamografia_unilateral_hospital",
        "1010593": "mamografia_unilateral_hospital",
        "1014146": "mamografia_unilateral_hospital",
        "80401110": "mamografia_unilateral_hospital",
        "17a2002002": "mastectomia_parcial_conservadora",
        "17d2002002": "mastectomia_parcial_conservadora",
        "1012162": "mastectomia_parcial_conservadora",
        "17a2002003": "mastectomia_radical_tardia",
        "17d2002003": "mastectomia_radical_tardia",
        "1012163": "mastectomia_radical_tardia",
    }

    orden_columnas_clinicas = [
        "mamografia_informada_aps",
        "mamografia_birads_0",
        "mamografia_birads_1_2",
        "mamografia_birads_3",
        "mamografia_birads_4_5_6",
        "mamografia_bilateral_hospital",
        "mamografia_unilateral_hospital",
        "mastectomia_parcial_conservadora",
        "mastectomia_radical_tardia",
    ]

    if ruta_encontrada is not None:
        tabla_base_mama = pd.read_parquet(ruta_encontrada)
        tabla_base_mama = tabla_base_mama.rename(
            columns={"year": "anio", "total": "cantidad_total"}
        )
        tabla_base_mama["cod_limpio"] = (
            tabla_base_mama["cod_prestacion"].astype(str).str.lstrip("0")
        )
        tabla_base_mama["prestacion"] = tabla_base_mama["cod_limpio"].map(
            mapa_columnas_limpias
        )
        tabla_base_mama["fecha"] = pd.to_datetime(
            dict(
                year=tabla_base_mama["anio"],
                month=tabla_base_mama["mes"],
                day=1,
            )
        )

        tabla_mensual_mama = (
            tabla_base_mama.pivot_table(
                index="fecha",
                columns="prestacion",
                values="cantidad_total",
                aggfunc="sum",
            )
            .fillna(0)
        )
        columnas_disponibles = [
            nombre for nombre in orden_columnas_clinicas if nombre in tabla_mensual_mama.columns
        ]
        tabla_mensual_mama = tabla_mensual_mama[columnas_disponibles]
        tabla_mensual_mama.columns.name = None
        tabla_mensual_mama.index.name = "fecha"

        tabla_anual_mama = tabla_mensual_mama.resample("YE").sum()
        tabla_anual_mama["anio"] = tabla_anual_mama.index.year
        tabla_anual_mama = tabla_anual_mama.set_index("anio")
        return tabla_mensual_mama, tabla_anual_mama

    # Respaldo anual pre-cargado 2015-2025 en caso de ejecutarse sin archivo externo
    datos_respaldo_anual = [
        {"anio": 2015, "mamografia_informada_aps": 313215, "mamografia_birads_0": 36476, "mamografia_birads_1_2": 238450, "mamografia_birads_3": 31430, "mamografia_birads_4_5_6": 1977, "mamografia_bilateral_hospital": 138664, "mamografia_unilateral_hospital": 6832, "mastectomia_parcial_conservadora": 2591, "mastectomia_radical_tardia": 2743},
        {"anio": 2016, "mamografia_informada_aps": 311326, "mamografia_birads_0": 35969, "mamografia_birads_1_2": 236177, "mamografia_birads_3": 33657, "mamografia_birads_4_5_6": 1780, "mamografia_bilateral_hospital": 140233, "mamografia_unilateral_hospital": 6992, "mastectomia_parcial_conservadora": 3018, "mastectomia_radical_tardia": 2563},
        {"anio": 2017, "mamografia_informada_aps": 342935, "mamografia_birads_0": 40919, "mamografia_birads_1_2": 256950, "mamografia_birads_3": 35838, "mamografia_birads_4_5_6": 2395, "mamografia_bilateral_hospital": 150600, "mamografia_unilateral_hospital": 9150, "mastectomia_parcial_conservadora": 3225, "mastectomia_radical_tardia": 2774},
        {"anio": 2018, "mamografia_informada_aps": 369542, "mamografia_birads_0": 42563, "mamografia_birads_1_2": 281291, "mamografia_birads_3": 38033, "mamografia_birads_4_5_6": 2172, "mamografia_bilateral_hospital": 156598, "mamografia_unilateral_hospital": 9075, "mastectomia_parcial_conservadora": 3493, "mastectomia_radical_tardia": 2926},
        {"anio": 2019, "mamografia_informada_aps": 402964, "mamografia_birads_0": 44491, "mamografia_birads_1_2": 307168, "mamografia_birads_3": 43186, "mamografia_birads_4_5_6": 2265, "mamografia_bilateral_hospital": 189170, "mamografia_unilateral_hospital": 9663, "mastectomia_parcial_conservadora": 3992, "mastectomia_radical_tardia": 2837},
        {"anio": 2020, "mamografia_informada_aps": 223465, "mamografia_birads_0": 25235, "mamografia_birads_1_2": 166408, "mamografia_birads_3": 25245, "mamografia_birads_4_5_6": 1581, "mamografia_bilateral_hospital": 104781, "mamografia_unilateral_hospital": 8791, "mastectomia_parcial_conservadora": 3010, "mastectomia_radical_tardia": 2260},
        {"anio": 2021, "mamografia_informada_aps": 415515, "mamografia_birads_0": 45253, "mamografia_birads_1_2": 312211, "mamografia_birads_3": 41235, "mamografia_birads_4_5_6": 3030, "mamografia_bilateral_hospital": 185115, "mamografia_unilateral_hospital": 11390, "mastectomia_parcial_conservadora": 3419, "mastectomia_radical_tardia": 2619},
        {"anio": 2022, "mamografia_informada_aps": 500318, "mamografia_birads_0": 53258, "mamografia_birads_1_2": 380423, "mamografia_birads_3": 51744, "mamografia_birads_4_5_6": 3493, "mamografia_bilateral_hospital": 238345, "mamografia_unilateral_hospital": 12601, "mastectomia_parcial_conservadora": 4186, "mastectomia_radical_tardia": 3301},
        {"anio": 2023, "mamografia_informada_aps": 604380, "mamografia_birads_0": 63784, "mamografia_birads_1_2": 455661, "mamografia_birads_3": 61185, "mamografia_birads_4_5_6": 4277, "mamografia_bilateral_hospital": 282240, "mamografia_unilateral_hospital": 15859, "mastectomia_parcial_conservadora": 4897, "mastectomia_radical_tardia": 3398},
        {"anio": 2024, "mamografia_informada_aps": 644868, "mamografia_birads_0": 63931, "mamografia_birads_1_2": 492546, "mamografia_birads_3": 65288, "mamografia_birads_4_5_6": 4695, "mamografia_bilateral_hospital": 299481, "mamografia_unilateral_hospital": 18161, "mastectomia_parcial_conservadora": 4901, "mastectomia_radical_tardia": 3257},
        {"anio": 2025, "mamografia_informada_aps": 546068, "mamografia_birads_0": 49546, "mamografia_birads_1_2": 423578, "mamografia_birads_3": 52767, "mamografia_birads_4_5_6": 3875, "mamografia_bilateral_hospital": 315937, "mamografia_unilateral_hospital": 18821, "mastectomia_parcial_conservadora": 5314, "mastectomia_radical_tardia": 3262},
    ]
    tabla_anual_mama = pd.DataFrame(datos_respaldo_anual).set_index("anio")
    return None, tabla_anual_mama


@st.cache_data
def cargar_datos_tamizaje_emp_50_59():
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    rutas_candidatas = [
        os.path.join(directorio_actual, "datos_analisis_mama_edad_2015_2025.parquet"),
        os.path.join(directorio_actual, "..", "datos_analisis_mama_edad_2015_2025.parquet"),
        "datos_analisis_mama_edad_2015_2025.parquet",
        "../datos_analisis_mama_edad_2015_2025.parquet",
        "G:/Mi unidad/do/datopia/deis-rem/datos_analisis_mama_edad_2015_2025.parquet",
    ]

    ruta_encontrada = None
    for ruta_posible in rutas_candidatas:
        if os.path.exists(ruta_posible):
            ruta_encontrada = ruta_posible
            break

    if ruta_encontrada is not None:
        tabla_base_edad = pd.read_parquet(ruta_encontrada)
        codigos_informadas_aps = {"18090600", "17150200", "29000008"}
        filtro_informadas_edad = (
            tabla_base_edad["cod_prestacion"].astype(str).isin(codigos_informadas_aps)
        )
        tabla_edad_informadas = tabla_base_edad[filtro_informadas_edad]

        resumen_anual_emp = (
            tabla_edad_informadas[
                tabla_edad_informadas["cod_col_numerica"].isin(["col01", "col04", "col05"])
            ]
            .groupby(["anio", "cod_col_numerica"])["cantidad_total"]
            .sum()
            .unstack("cod_col_numerica")
            .fillna(0)
        )
        resumen_anual_emp = resumen_anual_emp.rename(
            columns={
                "col01": "total_aps",
                "col04": "tramo_50_54",
                "col05": "tramo_55_59",
            }
        )
        resumen_anual_emp.columns.name = None
    else:
        datos_respaldo_emp = [
            {"anio": 2015, "total_aps": 313215, "tramo_50_54": 87479, "tramo_55_59": 65619},
            {"anio": 2016, "total_aps": 311326, "tramo_50_54": 79718, "tramo_55_59": 61775},
            {"anio": 2017, "total_aps": 342935, "tramo_50_54": 83505, "tramo_55_59": 68737},
            {"anio": 2018, "total_aps": 369542, "tramo_50_54": 85405, "tramo_55_59": 74838},
            {"anio": 2019, "total_aps": 402964, "tramo_50_54": 90556, "tramo_55_59": 80870},
            {"anio": 2020, "total_aps": 223465, "tramo_50_54": 48423, "tramo_55_59": 43771},
            {"anio": 2021, "total_aps": 415515, "tramo_50_54": 88741, "tramo_55_59": 82541},
            {"anio": 2022, "total_aps": 500318, "tramo_50_54": 100933, "tramo_55_59": 100197},
            {"anio": 2023, "total_aps": 604380, "tramo_50_54": 117847, "tramo_55_59": 116963},
            {"anio": 2024, "total_aps": 644868, "tramo_50_54": 126871, "tramo_55_59": 122792},
            {"anio": 2025, "total_aps": 546068, "tramo_50_54": 107319, "tramo_55_59": 103052},
        ]
        resumen_anual_emp = pd.DataFrame(datos_respaldo_emp).set_index("anio")

    resumen_anual_emp["total_emp_50_59"] = (
        resumen_anual_emp["tramo_50_54"] + resumen_anual_emp["tramo_55_59"]
    )
    resumen_anual_emp["porcentaje_emp"] = (
        resumen_anual_emp["total_emp_50_59"] / resumen_anual_emp["total_aps"]
    ) * 100
    return resumen_anual_emp


DICCIONARIO_MACROZONAS_CHILE = {
    "arica y parinacota": "Macrozona Norte",
    "tarapaca": "Macrozona Norte",
    "antofagasta": "Macrozona Norte",
    "atacama": "Macrozona Norte",
    "coquimbo": "Macrozona Norte",
    "valparaiso": "Macrozona Centro (sin RM)",
    "libertador general bernardo o'higgins": "Macrozona Centro (sin RM)",
    "maule": "Macrozona Centro (sin RM)",
    "metropolitana de santiago": "Región Metropolitana",
    "ñuble": "Macrozona Sur",
    "biobio": "Macrozona Sur",
    "la araucania": "Macrozona Sur",
    "los rios": "Macrozona Sur",
    "los lagos": "Macrozona Sur",
    "aysen del general carlos ibañez del campo": "Macrozona Austral",
    "magallanes y de la antartica chilena": "Macrozona Austral",
}

ORDEN_MACROZONAS = [
    "Región Metropolitana",
    "Macrozona Sur",
    "Macrozona Centro (sin RM)",
    "Macrozona Norte",
    "Macrozona Austral",
]


def _colores_macrozonas():
    estilo = CONFIGURACION_ESTILO
    return {
        "Región Metropolitana": estilo["color_tinta"],
        "Macrozona Sur": estilo["color_azul_clinico"],
        "Macrozona Centro (sin RM)": estilo["color_grafico_secundario"],
        "Macrozona Norte": "#3D7A74",
        "Macrozona Austral": estilo["color_rosa_apagado"],
    }


def _buscar_archivo_datos(nombre_archivo):
    directorio_actual = os.path.dirname(os.path.abspath(__file__))
    rutas_candidatas = [
        os.path.join(directorio_actual, nombre_archivo),
        os.path.join(directorio_actual, "..", nombre_archivo),
        nombre_archivo,
        os.path.join("..", nombre_archivo),
        f"G:/Mi unidad/do/datopia/deis-rem/{nombre_archivo}",
    ]
    for ruta_posible in rutas_candidatas:
        if os.path.exists(ruta_posible):
            return ruta_posible
    return None


@st.cache_data
def cargar_datos_tamizaje_macrozona():
    ruta_encontrada = _buscar_archivo_datos("datos_tamizaje_region_2015_2025.parquet")

    if ruta_encontrada is not None:
        tabla_region = pd.read_parquet(ruta_encontrada)
        tabla_region["macrozona"] = (
            tabla_region["region"].astype(str).str.lower().map(DICCIONARIO_MACROZONAS_CHILE)
        )
        tabla_region = tabla_region.dropna(subset=["macrozona"])
        tabla_anual_macro = (
            tabla_region.groupby(["anio", "macrozona"], as_index=False)["cantidad_total"]
            .sum()
        )
    else:
        anios_respaldo = list(range(2015, 2026))
        valores_respaldo_tamizaje = {
            "Región Metropolitana": [119341, 122318, 114302, 133450, 137212, 76106, 130457, 166814, 192210, 207991, 179020],
            "Macrozona Sur": [89754, 87257, 102235, 104000, 120933, 67174, 127263, 147423, 178212, 201001, 159730],
            "Macrozona Centro (sin RM)": [68892, 67077, 79696, 92153, 97880, 49620, 96874, 120899, 146520, 152564, 124098],
            "Macrozona Norte": [31119, 31312, 41722, 33986, 41638, 27694, 51750, 57472, 79060, 74199, 74458],
            "Macrozona Austral": [4109, 3362, 4980, 5953, 5301, 2871, 9171, 7710, 8378, 9113, 8762],
        }
        filas_respaldo = [
            {
                "anio": anio_valor,
                "macrozona": nombre_macrozona,
                "cantidad_total": serie_valores[indice_anio],
            }
            for nombre_macrozona, serie_valores in valores_respaldo_tamizaje.items()
            for indice_anio, anio_valor in enumerate(anios_respaldo)
        ]
        tabla_anual_macro = pd.DataFrame(filas_respaldo)

    tabla_base_2019 = (
        tabla_anual_macro[tabla_anual_macro["anio"] == 2019]
        .set_index("macrozona")["cantidad_total"]
        .rename("base_2019")
    )
    tabla_anual_macro = tabla_anual_macro.merge(
        tabla_base_2019, on="macrozona", how="left"
    )
    tabla_anual_macro["indice_base"] = (
        tabla_anual_macro["cantidad_total"] / tabla_anual_macro["base_2019"]
    ) * 100
    return tabla_anual_macro.sort_values(["anio", "macrozona"]).reset_index(drop=True)


@st.cache_data
def cargar_datos_cirugia_macrozona():
    ruta_encontrada = _buscar_archivo_datos("datos_cirugia_region_2015_2025.parquet")

    mapa_tipos_cirugia = {
        "17a2002002": "Mastectomía Parcial",
        "17d2002002": "Mastectomía Parcial",
        "1012162": "Mastectomía Parcial",
        "17a2002003": "Mastectomía Radical",
        "17d2002003": "Mastectomía Radical",
        "1012163": "Mastectomía Radical",
    }

    if ruta_encontrada is not None:
        tabla_cirugia_region = pd.read_parquet(ruta_encontrada)
        tabla_cirugia_region["macrozona"] = (
            tabla_cirugia_region["region"]
            .astype(str)
            .str.lower()
            .map(DICCIONARIO_MACROZONAS_CHILE)
        )
        tabla_cirugia_region["tipo_cirugia"] = (
            tabla_cirugia_region["cod_prestacion"]
            .astype(str)
            .str.lstrip("0")
            .map(mapa_tipos_cirugia)
        )
        tabla_cirugia_region = tabla_cirugia_region.dropna(
            subset=["macrozona", "tipo_cirugia"]
        )
        tabla_cirugia_macro = (
            tabla_cirugia_region.groupby(
                ["anio", "tipo_cirugia", "macrozona"], as_index=False
            )["cantidad_total"]
            .sum()
        )
    else:
        anios_respaldo = list(range(2015, 2026))
        valores_respaldo_cirugia = {
            ("Mastectomía Parcial", "Región Metropolitana"): [1102, 1356, 1395, 1538, 1708, 1254, 1436, 1748, 2078, 2039, 2104],
            ("Mastectomía Parcial", "Macrozona Sur"): [804, 897, 1030, 1011, 1111, 787, 917, 1152, 1311, 1154, 1427],
            ("Mastectomía Parcial", "Macrozona Centro (sin RM)"): [447, 531, 471, 539, 627, 559, 495, 684, 704, 827, 853],
            ("Mastectomía Parcial", "Macrozona Norte"): [207, 192, 261, 315, 453, 340, 498, 476, 645, 737, 769],
            ("Mastectomía Parcial", "Macrozona Austral"): [31, 42, 68, 90, 93, 70, 73, 126, 159, 144, 161],
            ("Mastectomía Radical", "Región Metropolitana"): [1185, 1135, 1282, 1233, 1148, 962, 1144, 1487, 1478, 1353, 1306],
            ("Mastectomía Radical", "Macrozona Sur"): [620, 568, 605, 739, 651, 553, 671, 766, 776, 787, 783],
            ("Mastectomía Radical", "Macrozona Centro (sin RM)"): [654, 599, 580, 639, 695, 506, 465, 664, 818, 800, 849],
            ("Mastectomía Radical", "Macrozona Norte"): [258, 245, 281, 288, 307, 219, 320, 360, 303, 297, 299],
            ("Mastectomía Radical", "Macrozona Austral"): [26, 16, 26, 27, 36, 20, 19, 24, 23, 20, 25],
        }
        filas_respaldo = [
            {
                "anio": anio_valor,
                "tipo_cirugia": nombre_tipo,
                "macrozona": nombre_macrozona,
                "cantidad_total": serie_valores[indice_anio],
            }
            for (nombre_tipo, nombre_macrozona), serie_valores in valores_respaldo_cirugia.items()
            for indice_anio, anio_valor in enumerate(anios_respaldo)
        ]
        tabla_cirugia_macro = pd.DataFrame(filas_respaldo)

    return tabla_cirugia_macro.sort_values(
        ["anio", "tipo_cirugia", "macrozona"]
    ).reset_index(drop=True)


# ==============================================================================
# CONSTRUCCION DE GRAFICOS INTERACTIVOS CON PLOTLY (DESIGN SYSTEM CLINICO LIMPIO)
# ==============================================================================

def crear_grafico_tamizaje_mensual(tabla_mensual_mama):
    estilo = CONFIGURACION_ESTILO
    minimo_abril_2020 = int(
        tabla_mensual_mama.loc["2020-04-01", "mamografia_informada_aps"]
    )
    fechas_texto_mensual = tabla_mensual_mama.index.strftime("%Y-%m-%d")
    anios_serie = range(
        int(tabla_mensual_mama.index.year.min()),
        int(tabla_mensual_mama.index.year.max()) + 1,
    )
    fechas_separadoras_anio = [f"{anio_actual}-01-01" for anio_actual in anios_serie] + [
        fechas_texto_mensual[-1]
    ]
    fechas_centradas_anio = [f"{anio_actual}-07-01" for anio_actual in anios_serie]
    etiquetas_anios = [str(anio_actual) for anio_actual in anios_serie]

    figura_tamizaje = go.Figure()

    figura_tamizaje.add_trace(
        go.Scatter(
            x=fechas_texto_mensual,
            y=tabla_mensual_mama["mamografia_informada_aps"],
            mode="lines+markers",
            name="Mamografías Informadas APS",
            line=dict(color=estilo["color_azul_clinico"], width=3, shape="spline"),
            marker=dict(size=5, color=estilo["color_azul_clinico"]),
            fill="tozeroy",
            fillcolor="rgba(46, 107, 138, 0.08)",
        )
    )

    figura_tamizaje.add_vrect(
        x0="2020-03-01",
        x1="2020-08-31",
        fillcolor=estilo["color_sombreado_cuarentena"],
        layer="below",
        line_width=0,
        annotation_text="Cuarentenas COVID-19",
        annotation_position="top left",
    )

    # Lineas verticales suaves al inicio de cada año y al cierre de la serie
    for fecha_separador in fechas_separadoras_anio:
        figura_tamizaje.add_shape(
            type="line",
            x0=fecha_separador,
            x1=fecha_separador,
            y0=0,
            y1=1,
            xref="x",
            yref="paper",
            layer="below",
            line=dict(color="rgba(12, 35, 64, 0.16)", width=1, dash="dot"),
        )

    figura_tamizaje.add_annotation(
        x="2020-04-01",
        y=minimo_abril_2020,
        text=f"Abril 2020: {minimo_abril_2020:,} controles".replace(",", "."),
        showarrow=True,
        arrowhead=2,
        arrowcolor=estilo["color_rosa_apagado"],
        arrowwidth=2,
        ax=55,
        ay=-45,
        bgcolor=estilo["color_superficie_rosa"],
        bordercolor=estilo["color_rosa_apagado"],
        borderwidth=1.5,
    )

    figura_tamizaje.update_layout(
        title=dict(
            text="Tamizaje Preventivo de Cáncer de Mama en APS (2015-2025)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Fecha (Mes y Año)",
        yaxis_title="Mamografías Informadas",
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            type="date",
            range=[fechas_texto_mensual[0], fechas_texto_mensual[-1]],
            tickvals=fechas_centradas_anio,
            ticktext=etiquetas_anios,
            showgrid=False,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_tamizaje


def crear_grafico_birads_anual(tabla_anual_mama):
    estilo = CONFIGURACION_ESTILO
    anios_mama = tabla_anual_mama.index
    casos_birads_sospecha = tabla_anual_mama["mamografia_birads_4_5_6"]

    figura_birads = go.Figure()

    textos_barras = [
        f"{int(valor):,}".replace(",", ".") for valor in casos_birads_sospecha
    ]

    figura_birads.add_trace(
        go.Bar(
            x=anios_mama,
            y=casos_birads_sospecha,
            name="BIRADS 4-5-6 Anuales",
            marker=dict(
                color=estilo["color_rosa_apagado"],
                cornerradius=8,
            ),
            text=textos_barras,
            textposition="outside",
        )
    )

    linea_base_2019 = tabla_anual_mama.loc[2019, "mamografia_birads_4_5_6"]
    texto_linea_base = f"Línea Base 2019 ({int(linea_base_2019):,} casos)".replace(
        ",", "."
    )

    figura_birads.add_trace(
        go.Scatter(
            x=[anios_mama[0], anios_mama[-1]],
            y=[linea_base_2019, linea_base_2019],
            mode="lines",
            name=texto_linea_base,
            line=dict(color=estilo["color_tinta"], width=1.8, dash="dot"),
        )
    )

    figura_birads.update_layout(
        title=dict(
            text="Sospecha o Certeza de Malignidad (BIRADS 4, 5 y 6)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Año",
        yaxis_title="Casos BIRADS 4, 5 o 6",
        yaxis_range=[0, max(casos_birads_sospecha) * 1.24],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        xaxis=dict(
            dtick=1,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_birads


def crear_grafico_indice_macrozona(tabla_anual_macro):
    estilo = CONFIGURACION_ESTILO
    colores_macro = _colores_macrozonas()
    figura_macrozona = go.Figure()

    for nombre_macrozona in ORDEN_MACROZONAS:
        subconjunto_macro = tabla_anual_macro[
            tabla_anual_macro["macrozona"] == nombre_macrozona
        ].sort_values("anio")
        volumenes_texto = [
            f"{int(round(valor_real)):,}".replace(",", ".")
            for valor_real in subconjunto_macro["cantidad_total"]
        ]
        figura_macrozona.add_trace(
            go.Scatter(
                x=subconjunto_macro["anio"],
                y=subconjunto_macro["indice_base"].round(1),
                mode="lines+markers",
                name=nombre_macrozona,
                customdata=volumenes_texto,
                line=dict(color=colores_macro[nombre_macrozona], width=2.8),
                marker=dict(size=6, color=colores_macro[nombre_macrozona]),
                hovertemplate=(
                    "%{y:.1f} pts (Volumen real: %{customdata} exámenes)<extra></extra>"
                ),
            )
        )

    figura_macrozona.add_hline(
        y=100,
        line_dash="dot",
        line_color=estilo["color_tinta"],
        line_width=1.6,
        annotation_text="Nivel prepandemia (2019 = 100)",
        annotation_position="bottom right",
    )

    figura_macrozona.update_layout(
        title=dict(
            text="Evolución Relativa del Tamizaje APS por Macrozona (Índice Base 2019 = 100)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Año",
        yaxis_title="Índice (Año 2019 = 100)",
        yaxis_range=[0, float(tabla_anual_macro["indice_base"].max()) * 1.16],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            dtick=1,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255, 255, 255, 0.85)",
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_macrozona


def crear_grafico_cirugia_macrozona(tabla_cirugia_macro):
    estilo = CONFIGURACION_ESTILO
    colores_macro = _colores_macrozonas()
    tipos_cirugia_panel = ["Mastectomía Parcial", "Mastectomía Radical"]

    totales_por_tipo_anio = (
        tabla_cirugia_macro.groupby(["tipo_cirugia", "anio"])["cantidad_total"]
        .sum()
        .rename("total_anio_tipo")
    )
    tabla_con_total = tabla_cirugia_macro.merge(
        totales_por_tipo_anio, on=["tipo_cirugia", "anio"], how="left"
    )
    maximo_eje_cirugia = float(totales_por_tipo_anio.max())

    figura_cirugia_macro = make_subplots(
        rows=1,
        cols=2,
        shared_yaxes=True,
        horizontal_spacing=0.05,
        subplot_titles=tuple(tipos_cirugia_panel),
    )

    for indice_panel, nombre_tipo_cirugia in enumerate(tipos_cirugia_panel, start=1):
        subconjunto_tipo = tabla_con_total[
            tabla_con_total["tipo_cirugia"] == nombre_tipo_cirugia
        ]
        for indice_macro, nombre_macrozona in enumerate(ORDEN_MACROZONAS):
            subconjunto_barra = subconjunto_tipo[
                subconjunto_tipo["macrozona"] == nombre_macrozona
            ].sort_values("anio")

            textos_detalle_hover = []
            for cantidad_fila, total_fila in zip(
                subconjunto_barra["cantidad_total"],
                subconjunto_barra["total_anio_tipo"],
            ):
                porcentaje_fila = (cantidad_fila / total_fila) * 100 if total_fila else 0
                cantidad_str = f"{int(round(cantidad_fila)):,}".replace(",", ".")
                porcentaje_str = f"{porcentaje_fila:.1f}%".replace(".", ",")
                textos_detalle_hover.append(f"{cantidad_str} ({porcentaje_str})")

            propiedades_barra = dict(color=colores_macro[nombre_macrozona])
            if indice_macro == len(ORDEN_MACROZONAS) - 1:
                propiedades_barra["cornerradius"] = 6

            figura_cirugia_macro.add_trace(
                go.Bar(
                    x=subconjunto_barra["anio"],
                    y=subconjunto_barra["cantidad_total"],
                    name=nombre_macrozona,
                    legendgroup=nombre_macrozona,
                    showlegend=(indice_panel == 1),
                    marker=propiedades_barra,
                    customdata=textos_detalle_hover,
                    hovertemplate="%{customdata} cirugías<extra></extra>",
                ),
                row=1,
                col=indice_panel,
            )

    figura_cirugia_macro.update_annotations(
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_leyenda_grafico"],
            color=estilo["color_tinta"],
        )
    )

    figura_cirugia_macro.update_layout(
        barmode="stack",
        title=dict(
            text="Evolución Quirúrgica por Macrozona: Parcial vs Radical (2015-2025)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        legend=dict(
            yanchor="top",
            y=0.97,
            xanchor="left",
            x=0.54,
            bgcolor="rgba(255, 255, 255, 0.90)",
            traceorder="reversed",
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=85, b=20),
        height=estilo["altura_grafico"],
    )

    figura_cirugia_macro.update_xaxes(
        title_text="Año",
        dtick=1,
        tickfont=dict(size=estilo["tamano_numeros_ejes"]),
        title_font=dict(size=estilo["tamano_ejes_grafico"]),
    )
    figura_cirugia_macro.update_yaxes(
        range=[0, maximo_eje_cirugia * 1.18],
        tickfont=dict(size=estilo["tamano_numeros_ejes"]),
        title_font=dict(size=estilo["tamano_ejes_grafico"]),
    )
    figura_cirugia_macro.update_yaxes(
        title_text="Intervenciones Quirúrgicas",
        row=1,
        col=1,
    )
    return figura_cirugia_macro


def crear_grafico_indice_ruta_clinica(tabla_anual_mama):
    estilo = CONFIGURACION_ESTILO
    columnas_ruta_indice = [
        "mamografia_informada_aps",
        "mamografia_birads_4_5_6",
        "mamografia_bilateral_hospital",
        "mastectomia_parcial_conservadora",
        "mastectomia_radical_tardia",
    ]
    etiquetas_ruta_indice = {
        "mamografia_informada_aps": "Tamizaje informado APS",
        "mamografia_birads_4_5_6": "BI-RADS 4-5-6 (sospecha)",
        "mamografia_bilateral_hospital": "Bilateral (Hosp. y Municipal)",
        "mastectomia_parcial_conservadora": "Mastectomía parcial",
        "mastectomia_radical_tardia": "Mastectomía radical",
    }
    colores_ruta_indice = {
        "mamografia_informada_aps": estilo["color_azul_clinico"],
        "mamografia_birads_4_5_6": estilo["color_rosa_apagado"],
        "mamografia_bilateral_hospital": estilo["color_grafico_secundario"],
        "mastectomia_parcial_conservadora": "#3D7A74",
        "mastectomia_radical_tardia": estilo["color_tinta"],
    }

    tabla_indice_2019 = (
        tabla_anual_mama[columnas_ruta_indice]
        / tabla_anual_mama.loc[2019, columnas_ruta_indice]
    ) * 100

    figura_indice_ruta = go.Figure()
    for nombre_prestacion in columnas_ruta_indice:
        figura_indice_ruta.add_trace(
            go.Scatter(
                x=tabla_indice_2019.index,
                y=tabla_indice_2019[nombre_prestacion].round(1),
                mode="lines+markers",
                name=etiquetas_ruta_indice[nombre_prestacion],
                line=dict(color=colores_ruta_indice[nombre_prestacion], width=2.8),
                marker=dict(size=6),
            )
        )

    figura_indice_ruta.add_hline(
        y=100,
        line_dash="dot",
        line_color=estilo["color_tinta"],
        line_width=1.6,
        annotation_text="Nivel prepandemia (2019 = 100)",
        annotation_position="bottom right",
    )

    figura_indice_ruta.update_layout(
        title=dict(
            text="Evolución Relativa de la Ruta Clínica Oncomamaria (Índice Base 2019 = 100)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Año",
        yaxis_title="Índice (Año 2019 = 100)",
        yaxis_range=[0, tabla_indice_2019.max().max() * 1.12],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            dtick=1,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_indice_ruta


def crear_grafico_tasa_sospecha_birads(tabla_anual_mama):
    estilo = CONFIGURACION_ESTILO
    tasa_sospecha_por_mil = (
        tabla_anual_mama["mamografia_birads_4_5_6"]
        / tabla_anual_mama["mamografia_informada_aps"]
    ) * 1000
    tasa_base_2019 = float(tasa_sospecha_por_mil.loc[2019])

    figura_tasa_sospecha = go.Figure()
    figura_tasa_sospecha.add_trace(
        go.Scatter(
            x=tasa_sospecha_por_mil.index,
            y=tasa_sospecha_por_mil.round(2),
            mode="lines+markers+text",
            name="Tasa BI-RADS 4-5-6 por 1.000 informadas",
            line=dict(color=estilo["color_rosa_apagado"], width=3),
            marker=dict(size=8, color=estilo["color_rosa_apagado"]),
            text=[f"{valor:.1f}".replace(".", ",") for valor in tasa_sospecha_por_mil],
            textposition="top center",
        )
    )

    figura_tasa_sospecha.add_hline(
        y=tasa_base_2019,
        line_dash="dot",
        line_color=estilo["color_tinta"],
        line_width=1.6,
        annotation_text=f"Referencia 2019: {tasa_base_2019:.1f} por mil".replace(".", ","),
        annotation_position="bottom right",
    )

    figura_tasa_sospecha.update_layout(
        title=dict(
            text="Tasa de Sospecha Maligna en Tamizaje APS (2015-2025)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Año",
        yaxis_title="Casos por 1.000 mamografías",
        yaxis_range=[0, max(tasa_sospecha_por_mil) * 1.25],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            dtick=1,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(font=dict(size=estilo["tamano_leyenda_grafico"])),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_tasa_sospecha


def crear_grafico_estacionalidad_mensual(tabla_mensual_mama):
    estilo = CONFIGURACION_ESTILO
    nombres_meses = [
        "Ene", "Feb", "Mar", "Abr", "May", "Jun",
        "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
    ]
    tabla_base_mes = tabla_mensual_mama[["mamografia_informada_aps"]].copy()
    tabla_base_mes["anio_registro"] = tabla_base_mes.index.year
    tabla_base_mes["mes_numero"] = tabla_base_mes.index.month

    serie_prepandemia = (
        tabla_base_mes[tabla_base_mes["anio_registro"].between(2015, 2019)]
        .groupby("mes_numero")["mamografia_informada_aps"]
        .mean()
        .reindex(range(1, 13))
    )
    serie_pospandemia = (
        tabla_base_mes[tabla_base_mes["anio_registro"].between(2021, 2025)]
        .groupby("mes_numero")["mamografia_informada_aps"]
        .mean()
        .reindex(range(1, 13))
    )

    maximo_estacional = max(
        float(serie_prepandemia.max()),
        float(serie_pospandemia.max()),
    )

    figura_estacionalidad = go.Figure()

    figura_estacionalidad.add_vrect(
        x0=6.55,
        x1=7.45,
        fillcolor=estilo["color_sombreado_cuarentena"],
        layer="below",
        line_width=0,
        annotation_text="Corte agosto",
        annotation_position="top",
        annotation_font=dict(size=12, color=estilo["color_rosa_apagado"]),
    )

    figura_estacionalidad.add_trace(
        go.Scatter(
            x=nombres_meses,
            y=serie_prepandemia.round(0),
            mode="lines+markers",
            name="Prepandemia (2015-2019)",
            line=dict(color=estilo["color_rosa_apagado"], width=3, shape="spline"),
            marker=dict(size=7, color=estilo["color_rosa_apagado"]),
        )
    )

    figura_estacionalidad.add_trace(
        go.Scatter(
            x=nombres_meses,
            y=serie_pospandemia.round(0),
            mode="lines+markers",
            name="Pospandemia (2021-2025)",
            line=dict(color=estilo["color_azul_clinico"], width=3, shape="spline"),
            marker=dict(size=7, color=estilo["color_azul_clinico"]),
        )
    )

    figura_estacionalidad.update_layout(
        title=dict(
            text="Estacionalidad Mensual de Mamografías en APS (Promedio)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Mes del Año",
        yaxis_title="Promedio Mensual de Exámenes",
        yaxis_range=[0, maximo_estacional * 1.22],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_estacionalidad


def crear_grafico_tamizaje_emp_50_59(resumen_anual_emp):
    estilo = CONFIGURACION_ESTILO
    anios_emp = resumen_anual_emp.index
    base_emp_2019 = float(resumen_anual_emp.loc[2019, "total_emp_50_59"])

    etiquetas_totales_emp = []
    for cantidad_emp, participacion_emp in zip(
        resumen_anual_emp["total_emp_50_59"], resumen_anual_emp["porcentaje_emp"]
    ):
        numero_texto = f"{int(cantidad_emp):,}".replace(",", ".")
        porcentaje_texto = f"{participacion_emp:.1f}%".replace(".", ",")
        etiquetas_totales_emp.append(f"{numero_texto}<br>({porcentaje_texto})")

    figura_emp = go.Figure()

    figura_emp.add_trace(
        go.Bar(
            x=anios_emp,
            y=resumen_anual_emp["tramo_50_54"],
            name="Mujeres 50 a 54 años (col04)",
            marker=dict(color=estilo["color_azul_clinico"]),
        )
    )

    figura_emp.add_trace(
        go.Bar(
            x=anios_emp,
            y=resumen_anual_emp["tramo_55_59"],
            name="Mujeres 55 a 59 años (col05)",
            marker=dict(color=estilo["color_grafico_secundario"], cornerradius=6),
        )
    )

    figura_emp.add_trace(
        go.Scatter(
            x=anios_emp,
            y=resumen_anual_emp["total_emp_50_59"],
            mode="text",
            text=etiquetas_totales_emp,
            textposition="top center",
            textfont=dict(size=10.5, color=estilo["color_tinta"]),
            showlegend=False,
            hoverinfo="skip",
        )
    )

    figura_emp.add_trace(
        go.Scatter(
            x=[int(anios_emp[0]) - 0.4, int(anios_emp[-1]) + 0.4],
            y=[base_emp_2019, base_emp_2019],
            mode="lines",
            name=f"Línea base 2019 EMP ({int(base_emp_2019):,})".replace(",", "."),
            line=dict(color="rgba(12, 35, 64, 0.45)", width=1.6, dash="dot"),
            hoverinfo="skip",
        )
    )

    figura_emp.add_vline(
        x=2022.5,
        line_dash="dash",
        line_color="#3D7A74",
        line_width=1.6,
        layer="below",
        annotation_text="Ley 21.551 (sin orden médica)",
        annotation_position="top left",
        annotation_yshift=-4,
    )

    figura_emp.update_layout(
        barmode="stack",
        title=dict(
            text="Tamizaje Preventivo en Mujeres del EMP: 50 a 59 Años (2015-2025)",
            font=dict(size=estilo["tamano_titulo_grafico"]),
        ),
        xaxis_title="Año",
        yaxis_title="Mamografías informadas (50-59 años)",
        yaxis_range=[0, float(resumen_anual_emp["total_emp_50_59"].max()) * 1.35],
        font=dict(
            family=estilo["familia_fuente"],
            size=estilo["tamano_ejes_grafico"],
            color=estilo["color_tinta"],
        ),
        paper_bgcolor=estilo["color_fondo_tarjetas"],
        plot_bgcolor=estilo["color_fondo_tarjetas"],
        template=estilo["plantilla_plotly"],
        hovermode="x unified",
        xaxis=dict(
            dtick=1,
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        yaxis=dict(
            tickfont=dict(size=estilo["tamano_numeros_ejes"]),
            title_font=dict(size=estilo["tamano_ejes_grafico"]),
        ),
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            font=dict(size=estilo["tamano_leyenda_grafico"]),
        ),
        margin=dict(l=20, r=20, t=55, b=20),
        height=estilo["altura_grafico"],
    )
    return figura_emp
