import streamlit as st
from funciones import (
    mostrar_tabla_configurable,
    mostrar_bloque_codigo_y_tabla,
    mostrar_bloque_grafico,
    obtener_esquema_hechos,
    obtener_esquema_codigos,
    obtener_muestra_hechos,
    obtener_muestra_codigos,
    obtener_esquema_jerarquia_prestaciones,
    obtener_muestra_jerarquia_prestaciones,
    obtener_esquema_jerarquia_columnas,
    obtener_muestra_jerarquia_columnas,
    obtener_esquema_establecimientos,
    obtener_muestra_establecimientos,
    obtener_esquema_establecimientos_historial,
    obtener_muestra_establecimientos_historial,
    obtener_muestra_busqueda_mama,
    obtener_muestra_codigos_antiguos_mamografia,
    obtener_resumen_hojas_mamografia,
    cargar_datos_cancer_mama,
    cargar_datos_tamizaje_emp_50_59,
    crear_grafico_tamizaje_mensual,
    crear_grafico_birads_anual,
    crear_grafico_mastectomias_anual,
    crear_grafico_indice_ruta_clinica,
    crear_grafico_tasa_sospecha_birads,
    crear_grafico_mastectomias_lineas,
    crear_grafico_tamizaje_emp_50_59,
)


# ==============================================================================
# VISTAS DE CADA SECCION DEL DASHBOARD (DESIGN SYSTEM CLINICO LIMPIO)
# ==============================================================================

def renderizar_pestana_tablas():
    st.header("Estructura de Datos DEIS-REM")

    # Barra de navegacion horizontal para explorar las 6 tablas oficiales del repositorio DEIS-REM
    tabla_seleccionada = st.radio(
        "Seleccione la tabla a explorar",
        [
            "Hechos",
            "Codigos",
            "Prestaciones",
            "Columnas",
            "Establecimientos",
            "Establecimientos Historial",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

    if tabla_seleccionada == "Hechos":
        with st.container(border=False):
            st.subheader("Tabla de Hechos")
            mostrar_tabla_configurable(obtener_esquema_hechos())

        codigo_muestra_hechos = """con.sql(\"\"\"
    SELECT *
    FROM hechos
    WHERE year = 2024
    LIMIT 4
\"\"\").df()
"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_hechos,
            tabla_resultado=obtener_muestra_hechos(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Codigos":
        with st.container(border=False):
            st.subheader("Tabla de Códigos")
            mostrar_tabla_configurable(obtener_esquema_codigos())

        codigo_muestra_codigos = """con.sql(\"\"\"
    SELECT year, cod_hoja, 
        nombre_hoja, 
        nombre_seccion,
        nombre_prestacion, 
        cod_prestacion,
        cod_col_numerica, 
        nombre_col_numerica
    FROM codigos
    WHERE year = 2024
      AND cod_prestacion = '04025025'
    ORDER BY cod_col_numerica
    LIMIT 4
\"\"\").df()"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_codigos,
            tabla_resultado=obtener_muestra_codigos(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Prestaciones":
        with st.container(border=False):
            st.subheader("Tabla de Jerarquía de Prestaciones")
            mostrar_tabla_configurable(obtener_esquema_jerarquia_prestaciones())

        codigo_muestra_jerarquia_prestaciones = """con.sql(\"\"\"
    SELECT year, serie, 
        cod_hoja, 
        nombre_hoja,
        cod_prestacion, 
        nombre_prestacion,
        nivel, 
        ruta_jerarquica, 
        es_hoja
    FROM jerarquia_prestaciones
    WHERE year = 2024
      AND cod_prestacion IN ('04025025', '04025035', '09215613', '09222800', '28020530')
    LIMIT 4
\"\"\").df()"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_jerarquia_prestaciones,
            tabla_resultado=obtener_muestra_jerarquia_prestaciones(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Columnas":
        with st.container(border=False):
            st.subheader("Tabla de Jerarquía de Columnas")
            mostrar_tabla_configurable(obtener_esquema_jerarquia_columnas())

        codigo_muestra_jerarquia_columnas = """con.sql(\"\"\"
    SELECT year, serie, 
        cod_hoja, 
        cod_seccion,
        cod_col_numerica, 
        nivel_0, nivel_1,
        nivel_2, ruta_jerarquica
    FROM jerarquia_columnas
    WHERE year = 2024
      AND cod_hoja = 'A09'
      AND cod_seccion = 'I'
    ORDER BY cod_col_numerica
    LIMIT 4
\"\"\").df()"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_jerarquia_columnas,
            tabla_resultado=obtener_muestra_jerarquia_columnas(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Establecimientos":
        with st.container(border=False):
            st.subheader("Tabla de Establecimientos")
            mostrar_tabla_configurable(obtener_esquema_establecimientos())

        codigo_muestra_establecimientos = """con.sql(\"\"\"
    SELECT id_establecimiento, 
        id_establecimiento_antiguo,
        nombre, nombre_comuna, 
        id_comuna,
        nombre_servicio, 
        id_region,
        primera_aparicion, 
        ultima_aparicion
    FROM establecimientos
    LIMIT 4
\"\"\").df()"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_establecimientos,
            tabla_resultado=obtener_muestra_establecimientos(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Establecimientos Historial":
        with st.container(border=False):
            st.subheader("Tabla de Historial de Establecimientos")
            mostrar_tabla_configurable(obtener_esquema_establecimientos_historial())

        codigo_muestra_establecimientos_historial = """con.sql(\"\"\"
    SELECT anio, id_establecimiento, 
        id_establecimiento_antiguo,
        nombre, nombre_comuna, 
        id_comuna,
        nombre_servicio, id_region
    FROM establecimientos_historial
    WHERE anio = 2024
    LIMIT 4
\"\"\").df()"""

        mostrar_bloque_codigo_y_tabla(
            titulo_bloque="",
            descripcion_bloque="",
            codigo_ejemplo=codigo_muestra_establecimientos_historial,
            tabla_resultado=obtener_muestra_establecimientos_historial(),
            en_columnas=True,
        )


def renderizar_pestana_busqueda():
    st.header("Metodologia de Busqueda en el Catalogo Clinico")

    st.markdown(
        """
        <div class="tarjeta-bento tarjeta-superficie">
            <div style="margin-bottom: 12px;">
                <span class="pildora pildora-rosa">Cancer de Mama 2015 - 2025</span>
                <span class="pildora pildora-blanca">Alerta Sanitaria 2020</span>
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Contexto e Impacto de las Restricciones Sanitarias de 2020</h3>
            <p style="margin-bottom: 10px;">
                En marzo de 2020, ante la emergencia sanitaria por COVID-19, se declaró el estado de catástrofe, restringiendo el desplazamiento
                y postergando los controles preventivos y cirugías electivas para concentrar la red asistencial en la atención de la pandemia.
                Al suspenderse prestaciones de rutina como mamografías y PAP, este estudio busca cuantificar en los registros del DEIS el quiebre
                de atenciones preventivas en 2020 y la posterior acumulación diagnóstica y quirúrgica entre 2021 y 2025.
            </p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Ruta Clinica del Cancer de Mama en Chile")

    st.markdown(
        """
        <div class="ruta-clinica-contenedor">
        <div class="tarjeta-bento tarjeta-superficie">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 5px;">Tamizaje y Pesquisa Precoz en Atencion Primaria</h3>
            <p>
                <strong>Chequeos preventivos en consultorios y CESFAM:</strong>
                Mamografía preventiva gratuita para mujeres de 50 a 69 años, orientada a detectar lesiones antes de que presenten síntomas. Desde 2023 (Ley 21.551) se puede realizar sin necesidad de orden médica previa.
            </p>
        </div>

        <div class="tarjeta-bento tarjeta-blanca">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 14px;">Clasificacion Radiologica BI-RADS</h3>
            <div class="fila-item-bento">
                <div><strong>BI-RADS 0</strong> — Estudio incompleto </div>
                <span class="pildora pildora-suave">Complementar</span>
            </div>
            <div class="fila-item-bento">
                <div><strong>BI-RADS 1 y 2</strong> — Hallazgo normal o benigno</div>
                <span class="pildora pildora-clinica">Normal / Benigno</span>
            </div>
            <div class="fila-item-bento">
                <div><strong>BI-RADS 3</strong> — Probablemente benigno</div>
                <span class="pildora pildora-suave">Control 6 meses</span>
            </div>
            <div class="fila-item-bento">
                <div><strong>BI-RADS 4 y 5</strong> — Sospecha o alta probabilidad de malignidad</div>
                <span class="pildora pildora-rosa">Alerta GES / Biopsia</span>
            </div>
            <div class="fila-item-bento">
                <div><strong>BI-RADS 6</strong> — Malignidad ya confirmada</div>
                <span class="pildora pildora-oscura">Confirmado</span>
            </div>
        </div>

        <div class="tarjeta-bento tarjeta-rosa-alerta">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Confirmacion Diagnostica y Etapificacion</h3>
            <p style="margin-bottom: 0;">
                Ante un resultado <strong>BI-RADS 4 o 5</strong> o sospecha en examen fisico, la paciente ingresa a la Unidad de Patologia Mamaria hospitalaria.
                Contempla ecotomografia complementaria, confirmacion histologica mediante biopsia core o estereotaxica (<code>Hoja B</code> y etapificacion.
            </p>
        </div>

        <div class="tarjeta-bento tarjeta-blanca">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Tratamiento y Seguimiento</h3>
            <ul style="margin-bottom: 0;">
                <li><strong>Estadio temprano:</strong> Mastectomia parcial o conservadora (<code>Hoja B</code>, codigo <code>01012162</code>).</li>
                <li><strong>Estadio tardio:</strong> Mastectomia radical con vaciamiento axilar (<code>Hoja B</code>, codigo <code>01012163</code>).</li>
            </ul>
        </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    codigo_busqueda_antiguos = """
catalogo_mamografias = con.sql(\"\"\"
    SELECT 
        cod_hoja,
        cod_prestacion,
        ANY_VALUE(nombre_prestacion) AS nombre_prestacion,
        MIN(year) AS anio_inicio,
        MAX(year) AS anio_termino
    FROM codigos
    WHERE year BETWEEN 2015 AND 2025
      AND (
          nombre_prestacion ILIKE '%mamograf%'
          OR nombre_prestacion ILIKE '%birads%'
          OR (nombre_prestacion ILIKE '%mamog%' AND 
            nombre_prestacion ILIKE '%bilateral%')
          OR (nombre_prestacion ILIKE '%mamog%' AND 
            nombre_prestacion ILIKE '%unilateral%')
      )
    GROUP BY cod_hoja, cod_prestacion
    ORDER BY anio_inicio, cod_hoja, cod_prestacion
\"\"\").df()

display(catalogo_mamografias)"""

    mostrar_bloque_codigo_y_tabla(
        titulo_bloque="Exploración del catálogo mediante palabras claves por año",
        descripcion_bloque=(
            "Se busca directamente en el catálogo mediante palabras claves como **mamografia**, **bilateral**, **unilateral** y **birads** "
            "a través de los años (2015 a 2025), obteniendo el rango de vigencia de cada prestación:"
        ),
        codigo_ejemplo=codigo_busqueda_antiguos,
        tabla_resultado=obtener_muestra_codigos_antiguos_mamografia(),
        en_columnas=True,
    )

    with st.container(border=False):
        st.subheader("Sintesis de Hojas REM que Registran Mamografias y Cirugia Mamaria")
        st.markdown(
            "A partir de la exploracion del diccionario entre 2015 y 2025, se identifican las hojas clave del sistema DEIS-REM para el estudio de cancer de mama:"
        )
        mostrar_tabla_configurable(obtener_resumen_hojas_mamografia())


def renderizar_pestana_analisis_mama():
    st.header("Retraso Diagnostico y Quirurgico (2015 - 2025)")

    tabla_mensual_mama, tabla_anual_mama = cargar_datos_cancer_mama()
    tabla_anual_vista = tabla_anual_mama.round(0).astype(int).reset_index()

    with st.container(border=False):
        st.subheader("Consolidacion Historica de Prestaciones Oncomamarias (2015 - 2025)")
        mostrar_tabla_configurable(tabla_anual_vista, tipo_tabla="consolidacion")

    tamizaje_2024 = int(tabla_anual_mama.loc[2024, "mamografia_informada_aps"])
    tamizaje_2025 = int(tabla_anual_mama.loc[2025, "mamografia_informada_aps"])
    minimo_abril_2020 = (
        int(tabla_mensual_mama.loc["2020-04-01", "mamografia_informada_aps"])
        if tabla_mensual_mama is not None
        else 3533
    )

    birads_2019 = int(tabla_anual_mama.loc[2019, "mamografia_birads_4_5_6"])
    birads_2024 = int(tabla_anual_mama.loc[2024, "mamografia_birads_4_5_6"])
    birads_2025 = int(tabla_anual_mama.loc[2025, "mamografia_birads_4_5_6"])
    variacion_birads_2025 = ((birads_2025 - birads_2019) / birads_2019) * 100

    parciales_2025 = int(tabla_anual_mama.loc[2025, "mastectomia_parcial_conservadora"])
    radicales_2025 = int(tabla_anual_mama.loc[2025, "mastectomia_radical_tardia"])

    texto_minimo_abril = f"{minimo_abril_2020:,}".replace(",", ".")
    texto_tamizaje_2024 = f"{tamizaje_2024:,}".replace(",", ".")
    texto_tamizaje_2025 = f"{tamizaje_2025:,}".replace(",", ".")
    texto_birads_2024 = f"{birads_2024:,}".replace(",", ".")
    texto_birads_2025 = f"{birads_2025:,}".replace(",", ".")
    texto_var_birads_2025 = f"+{variacion_birads_2025:.1f}".replace(".", ",")
    texto_parciales_2025 = f"{parciales_2025:,}".replace(",", ".")
    texto_radicales_2025 = f"{radicales_2025:,}".replace(",", ".")

    if tabla_mensual_mama is not None:
        mostrar_bloque_grafico(
            titulo_grafico="Colapso del Tamizaje Preventivo en Cuarentenas (2020) y Evolucion Reciente (2025)",
            descripcion_previa=(
                f"Las mamografias informadas en APS cayeron a su minimo historico con {texto_minimo_abril} examenes en abril de 2020, tomando mas de 18 meses recuperar el nivel prepandemia. "
                f"Al extender la serie hasta **2025**, el registro en hoja A29 pasa de **{texto_tamizaje_2024}** en 2024 a **{texto_tamizaje_2025}** en 2025. "
            ),
            figura_plotly=crear_grafico_tamizaje_mensual(tabla_mensual_mama),
        )

    columna_graf_birads, columna_graf_cirugia = st.columns(2, gap="medium")

    with columna_graf_birads:
        mostrar_bloque_grafico(
            titulo_grafico="Deteccion de Hallazgos Sospechosos (BIRADS 4, 5 y 6)",
            descripcion_previa=(
                f"La caida de tamizaje en 2020 genero un subdiagnostico inicial (1.581 casos), seguido de una ola acumulada que alcanzo **4.277** casos en 2023 y **{texto_birads_2024}** en 2024 (mas del doble que 2019)."
            ),
            figura_plotly=crear_grafico_birads_anual(tabla_anual_mama),
        )

    with columna_graf_cirugia:
        mostrar_bloque_grafico(
            titulo_grafico="Evolucion Quirurgica",
            descripcion_previa=(
                f"Las mastectomias radicales con vaciamiento axilar alcanzaron su pico en **2023** (3.398 cirugias) y se mantienen estables en **2024** (3.257) y **2025** ({texto_radicales_2025}), mientras las cirugias parciales conservadoras crecen hasta un nuevo maximo historico en **2025** ({texto_parciales_2025} intervenciones)."
            ),
            figura_plotly=crear_grafico_mastectomias_anual(tabla_anual_mama),
        )

    mostrar_bloque_grafico(
        titulo_grafico="Comparacion Estandarizada de la Ruta Clinica (Indice Base 2019 = 100)",
        descripcion_previa=(
            "Normalizar cada etapa por su nivel de **2019 (= 100)** permite comparar en una misma escala. En **2020**, el tamizaje APS y las bilaterales cayeron cerca de **55 puntos**, mientras las cirugias descendieron menos (**75** parciales y **80** radicales) por priorizacion oncologica. Hacia **2024**, BI-RADS 4-5-6 llego a **207 puntos** y en **2025** las bilaterales totales (167) y parciales (133) marcan nuevos maximos relativos."
        ),
        figura_plotly=crear_grafico_indice_ruta_clinica(tabla_anual_mama),
    )

    columna_graf_tasa, columna_graf_proporcion = st.columns(2, gap="medium")

    with columna_graf_tasa:
        mostrar_bloque_grafico(
            titulo_grafico="Tasa de Sospecha por 1.000 Mamografias Informadas",
            descripcion_previa=(
                "Para aislar la carga de sospecha maligna sobre la poblacion efectivamente tamizada, se calcula la tasa por **1.000 informadas** dentro de la misma hoja A29. Previo a la pandemia oscilaba entre **5,6 y 6,3 por mil**, mientras entre **2020 y 2025** permanece elevada entre **7,0 y 7,3 por mil**."
            ),
            figura_plotly=crear_grafico_tasa_sospecha_birads(tabla_anual_mama),
        )

    with columna_graf_proporcion:
        mostrar_bloque_grafico(
            titulo_grafico="Evolucion de Mastectomias Radicales y Parciales",
            descripcion_previa=(
                f"Comparacion directa de la trayectoria anual en numero de cirugias. Las parciales mantienen un crecimiento sostenido desde **2.591 (2015)** hasta **{texto_parciales_2025} en 2025**, mientras las mastectomias radicales alcanzaron su maximo en **2023 (3.398)** y se mantienen en **2024 (3.257)** y **2025 ({texto_radicales_2025})**."
            ),
            figura_plotly=crear_grafico_mastectomias_lineas(tabla_anual_mama),
        )

    resumen_anual_emp = cargar_datos_tamizaje_emp_50_59()

    mostrar_bloque_grafico(
        titulo_grafico="Tamizaje Preventivo en Poblacion Objetivo del EMP: Mujeres de 50 a 59 Años (2015 - 2025)",
        descripcion_previa=(
            "El **Examen de Medicina Preventiva (EMP)** garantiza mamografia gratuita para mujeres entre **50 y 59 años**, "
            "tramo medido de manera estable desde 2015 hasta 2025 mediante las columnas **col04 (50-54 anios)** y **col05 (55-59 anios)** de BM18, BS17 y A29. "
            "Este grupo cayó de 171.426 en 2019 a 92.194 en 2020. "
            "En 2023 por la **Ley N° 21.551** elimina la orden medica, alcanzando un maximo historico de **249.663 examenes en 2024** "
            "(210.371 en 2025 por el subregistro parcial en seis Servicios de Salud)."
        ),
        figura_plotly=crear_grafico_tamizaje_emp_50_59(resumen_anual_emp),
    )
