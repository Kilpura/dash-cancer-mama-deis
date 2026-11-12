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
    crear_grafico_estacionalidad_mensual,
    crear_grafico_tamizaje_emp_50_59,
)


# ==============================================================================
# VISTAS DE CADA SECCION DEL DASHBOARD (DESIGN SYSTEM CLINICO LIMPIO)
# ==============================================================================


def renderizar_pestana_tablas():
    st.header("Estructura de Datos DEIS-REM")

    st.markdown(
        """
        <div class="mapa-tablas-contenedor">
            <div class="tarjeta-bento tarjeta-superficie">
                <span class="pildora pildora-clinica">Tabla central</span>
                <h3>Hechos (conteos mensuales)</h3>
                <p>Guarda cuántas atenciones se informaron cada mes y año. Como usa códigos numéricos, se apoya en los diccionarios para leerse.</p>
            </div>
            <div class="tarjeta-bento tarjeta-blanca">
                <span class="pildora pildora-suave">Qué se realizó</span>
                <h3>Códigos (el traductor)</h3>
                <p>Traduce el código de prestación y columna a texto clínico legible: qué examen o cirugía es y si mide hombres, mujeres o edad.</p>
            </div>
            <div class="tarjeta-bento tarjeta-blanca">
                <span class="pildora pildora-suave">Nivel de detalle</span>
                <h3>Prestaciones y Columnas</h3>
                <p>Desarman cada glosa en forma de árbol jerárquico, separando subgrupos de actividad, sexo, edad y tipo de conteo.</p>
            </div>
            <div class="tarjeta-bento tarjeta-rosa-alerta">
                <span class="pildora pildora-rosa">Dónde ocurrió</span>
                <h3>Establecimientos e Historial</h3>
                <p>Ubica cada código de recinto en su CESFAM, hospital, comuna y Servicio de Salud, rastreando cambios de nombre o código en el tiempo.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Barra de navegacion horizontal para explorar las 6 tablas oficiales del repositorio DEIS-REM
    tabla_seleccionada = st.radio(
        "Seleccione la tabla a explorar",
        [
            "Hechos",
            "Códigos",
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
            titulo_bloque="Ejemplo real: cómo se registra una misma atención",
            descripcion_bloque=(
                "La consulta toma cuatro filas de enero de 2024 para un mismo recinto (101010) y prestación (06020201). "
                "En la tabla de la derecha ves cómo el total de 22 atenciones (col01) se desglosa en 21 hombres (col02) y 1 mujer (col03)."
            ),
            codigo_ejemplo=codigo_muestra_hechos,
            tabla_resultado=obtener_muestra_hechos(),
            en_columnas=True,
        )

    elif tabla_seleccionada == "Códigos":
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
            titulo_bloque="Ejemplo real: qué significado esconde cada código",
            descripcion_bloque=(
                "Aquí consultamos la prestación 04025025 (atención de salud mental en la hoja A04 de 2024). "
                "La tabla muestra cómo la misma atención cambia de significado según la columna: total de ambos sexos (col01), hombres (col02), mujeres (col03) o tramo menor de 1 año (col04)."
            ),
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
            titulo_bloque="Ejemplo real: cómo se ordena el árbol de actividades",
            descripcion_bloque=(
                "La muestra revisa nodos iniciales de actividades del nivel 1 (como atenciones a personas de 65 años y más o actividades en colegios e instituciones) "
                "para ver cómo el formulario agrupa las glosas antes de llegar al detalle específico."
            ),
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
            titulo_bloque="Ejemplo real: desglose de atributos de columna",
            descripcion_bloque=(
                "Muestra cuatro registros de nivel 1 del catálogo de columnas, donde cada atributo (como acompañante o vínculo con el agresor) "
                "se separa en pares clave-valor ordenados para facilitar los cruces analíticos."
            ),
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
            titulo_bloque="Ejemplo real: ficha territorial de cada recinto",
            descripcion_bloque=(
                "Presenta cuatro códigos de establecimientos pertenecientes al Servicio de Salud Arica y Parinacota en la comuna de Arica, "
                "mostrando su tipo de centro, dependencia administrativa y nivel de complejidad."
            ),
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
            titulo_bloque="Ejemplo real: trazabilidad de cambios en el tiempo",
            descripcion_bloque=(
                "Sigue el historial del recinto 101010: muestra cuál era su código antiguo (01-010) y el periodo exacto de vigencia (year_inicio a year_termino) "
                "de cada tipo de establecimiento, condición y fecha de apertura."
            ),
            codigo_ejemplo=codigo_muestra_establecimientos_historial,
            tabla_resultado=obtener_muestra_establecimientos_historial(),
            en_columnas=True,
        )


def renderizar_pestana_busqueda():
    st.header("Metodología de Búsqueda en el Catálogo Clínico")

    st.markdown(
        """
        <div class="tarjeta-bento tarjeta-superficie">
            <div style="margin-bottom: 12px;">
                <span class="pildora pildora-rosa">Cáncer de Mama 2015 - 2025</span>
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

    st.subheader("Ruta Clínica del Cáncer de Mama en Chile")

    st.markdown(
        """
        <div class="ruta-clinica-contenedor">
        <div class="tarjeta-bento tarjeta-superficie">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 5px;">Tamizaje y Pesquisa Precoz en Atención Primaria</h3>
            <p>
                <strong>Chequeos preventivos en consultorios y CESFAM:</strong>
                Mamografía preventiva gratuita para mujeres de 50 a 69 años. Desde 2023 (Ley 21.551) se puede realizar sin necesidad de orden médica previa.
            </p>
        </div>

        <div class="tarjeta-bento tarjeta-blanca">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Clasificación Radiológica BI-RADS</h3>
            <div class="birads-semaforo-grid">
                <div class="birads-item-circulo">
                    <div class="birads-circulo birads-circulo-suave">0</div>
                    <div class="birads-titulo">Incompleto</div>
                    <div class="birads-subtitulo">Complementar</div>
                </div>
                <div class="birads-item-circulo">
                    <div class="birads-circulo birads-circulo-clinico">1 - 2</div>
                    <div class="birads-titulo">Normal</div>
                    <div class="birads-subtitulo">Hallazgo benigno</div>
                </div>
                <div class="birads-item-circulo">
                    <div class="birads-circulo birads-circulo-suave">3</div>
                    <div class="birads-titulo">Control 6m</div>
                    <div class="birads-subtitulo">Prob. benigno</div>
                </div>
                <div class="birads-item-circulo">
                    <div class="birads-circulo birads-circulo-rosa">4 - 5</div>
                    <div class="birads-titulo">Alerta GES</div>
                    <div class="birads-subtitulo">Sospecha biopsia</div>
                </div>
                <div class="birads-item-circulo">
                    <div class="birads-circulo birads-circulo-oscuro">6</div>
                    <div class="birads-titulo">Confirmado</div>
                    <div class="birads-subtitulo">Malignidad confirmada.</div>
                </div>
            </div>
        </div>

        <div class="tarjeta-bento tarjeta-rosa-alerta">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Confirmación Diagnóstica y Etapificación</h3>
            <p style="margin-bottom: 0;">
                Ante un resultado <strong>BI-RADS 4 o 5</strong> o sospecha en examen físico, la paciente ingresa a la Unidad de Patología Mamaria hospitalaria.
                Contempla confirmación histológica mediante biopsia core o estereotáxica (<code>Hoja B</code>) y etapificación.
            </p>
        </div>

        <div class="tarjeta-bento tarjeta-blanca">
            <div style="margin-bottom: 0px;">
            </div>
            <h3 style="margin-top: 0; margin-bottom: 10px;">Tratamiento y Seguimiento</h3>
            <ul style="margin-bottom: 0;">
                <li><strong>Estadio temprano:</strong> Mastectomía parcial o conservadora (<code>Hoja B</code>, código <code>01012162</code>).</li>
                <li><strong>Estadio tardío:</strong> Mastectomía radical con vaciamiento axilar (<code>Hoja B</code>, código <code>01012163</code>).</li>
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
            "Se busca directamente en el catálogo mediante palabras claves como **mamografía**, **bilateral**, **unilateral** y **birads** "
            "a través de los años (2015 a 2025), obteniendo el rango de vigencia de cada prestación:"
        ),
        codigo_ejemplo=codigo_busqueda_antiguos,
        tabla_resultado=obtener_muestra_codigos_antiguos_mamografia(),
        en_columnas=True,
    )

    with st.container(border=False):
        st.subheader("Síntesis de Hojas REM que Registran Mamografías y Cirugía Mamaria")
        st.markdown(
            "A partir de la exploración del diccionario entre 2015 y 2025, se identifican las hojas clave del sistema DEIS-REM para el estudio de cáncer de mama:"
        )
        mostrar_tabla_configurable(obtener_resumen_hojas_mamografia())


def renderizar_pestana_analisis_mama():
    st.header("Retraso Diagnóstico y Quirúrgico (2015 - 2025)")

    st.markdown(
        """
        <div class="tarjeta-bento tarjeta-superficie" style="margin-top: 0.75rem; margin-bottom: 1.5rem;">
            <h3 style="margin-top: 0; margin-bottom: 8px;">Conclusiones principales</h3>
            <ul style="margin-bottom: 0; padding-left: 20px;">
                <li><strong>Caída del tamizaje en 2020:</strong> Las mamografías preventivas en APS descendieron bruscamente durante las restricciones de 2020 y se recuperaron gradualmente hasta alcanzar máximos en 2023–2024.</li>
                <li><strong>Alza pospandemia en sospecha y cirugías:</strong> Desde 2021 se aprecia una tendencia creciente en hallazgos BI-RADS 4-5-6 y en intervenciones quirúrgicas (mastectomías parciales y radicales), debido aparentemente a la falta de mamografías oportunas durante la pandemia.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tabla_mensual_mama, tabla_anual_mama = cargar_datos_cancer_mama()
    tabla_anual_vista = tabla_anual_mama.round(0).astype(int).reset_index()

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
            titulo_grafico="Colapso del Tamizaje Preventivo en Cuarentenas (2020) y Evolución Reciente (2025)",
            descripcion_previa=(
                f"Las mamografías informadas en APS cayeron a su mínimo histórico con {texto_minimo_abril} exámenes en abril de 2020, tomando más de 18 meses recuperar el nivel prepandemia. "
                f"Al extender la serie hasta **2025**, el registro en hoja A29 pasa de **{texto_tamizaje_2024}** en 2024 a **{texto_tamizaje_2025}** en 2025. "
            ),
            figura_plotly=crear_grafico_tamizaje_mensual(tabla_mensual_mama),
        )

    columna_graf_birads, columna_graf_cirugia = st.columns(2, gap="medium")

    with columna_graf_birads:
        mostrar_bloque_grafico(
            titulo_grafico="Detección de Hallazgos Sospechosos (BIRADS 4, 5 y 6)",
            descripcion_previa=(
                f"La caída de tamizaje en 2020 generó un subdiagnóstico inicial (1.581 casos), seguido de una ola acumulada que alcanzó **4.277** casos en 2023 y **{texto_birads_2024}** en 2024 (más del doble que 2019)."
            ),
            figura_plotly=crear_grafico_birads_anual(tabla_anual_mama),
        )

    with columna_graf_cirugia:
        mostrar_bloque_grafico(
            titulo_grafico="Evolución Quirúrgica",
            descripcion_previa=(
                f"Las mastectomías radicales alcanzaron su máximo en **2023** (3.398 cirugías) y se mantienen estables en **2024** (3.257) y **2025** ({texto_radicales_2025}), mientras las cirugías parciales crecen hasta un nuevo máximo histórico en **2025** ({texto_parciales_2025} intervenciones)."
            ),
            figura_plotly=crear_grafico_mastectomias_anual(tabla_anual_mama),
        )

    mostrar_bloque_grafico(
        titulo_grafico="Comparación Estandarizada de la Ruta Clínica (Índice Base 2019 = 100)",
        descripcion_previa=(
            "Normalizar cada etapa por su nivel de **2019 (= 100)** permite comparar en una misma escala. En **2020**, el tamizaje APS y las bilaterales cayeron cerca de **55 puntos**, mientras las cirugías descendieron menos (**75** parciales y **80** radicales) por priorización oncológica. Hacia **2024**, BI-RADS 4-5-6 llegó a **207 puntos** y en **2025** las bilaterales totales (167) y parciales (133) marcan nuevos máximos relativos."
        ),
        figura_plotly=crear_grafico_indice_ruta_clinica(tabla_anual_mama),
    )

    columna_graf_tasa, columna_graf_estacionalidad = st.columns(2, gap="medium")

    with columna_graf_tasa:
        mostrar_bloque_grafico(
            titulo_grafico="Tasa de Sospecha por 1.000 Mamografías Informadas",
            descripcion_previa=(
                "Para aislar la carga de sospecha maligna sobre la población efectivamente tamizada, se calcula la tasa por **1.000 informadas** dentro de la misma hoja A29. Previo a la pandemia oscilaba entre **5,6 y 6,3 por mil**, mientras entre **2020 y 2025** permanece elevada entre **7,0 y 7,3 por mil**."
            ),
            figura_plotly=crear_grafico_tasa_sospecha_birads(tabla_anual_mama),
        )

    if tabla_mensual_mama is not None:
        with columna_graf_estacionalidad:
            mostrar_bloque_grafico(
                titulo_grafico="Estacionalidad Mensual del Tamizaje en APS",
                descripcion_previa=(
                    "Comparación del promedio mensual entre prepandemia (**2015-2019**) y pospandemia (**2021-2025**), excluyendo 2020 por el quiebre sanitario. "
                    "Tras los mínimos de enero y febrero, destaca un máximo recurrente en **agosto** asociado al corte de evaluación de metas en APS, seguido por la baja de septiembre y el cierre anual de noviembre-diciembre."
                ),
                figura_plotly=crear_grafico_estacionalidad_mensual(tabla_mensual_mama),
            )

    resumen_anual_emp = cargar_datos_tamizaje_emp_50_59()

    mostrar_bloque_grafico(
        titulo_grafico="Tamizaje Preventivo en Población Objetivo del EMP: Mujeres de 50 a 59 Años (2015 - 2025)",
        descripcion_previa=(
            "El **Examen de Medicina Preventiva (EMP)** garantiza mamografía gratuita para mujeres entre **50 y 59 años**, "
            "tramo medido de manera estable desde 2015 hasta 2025 mediante las columnas **col04 (50-54 años)** y **col05 (55-59 años)** de BM18, BS17 y A29. "
            "Este grupo cayó de 171.426 en 2019 a 92.194 en 2020. "
            "En 2023 por la **Ley N° 21.551** elimina la orden médica, alcanzando un máximo histórico de **249.663 exámenes en 2024** "
            "(210.371 en 2025 por el subregistro parcial en seis Servicios de Salud)."
        ),
        figura_plotly=crear_grafico_tamizaje_emp_50_59(resumen_anual_emp),
    )

    with st.container(border=False):
        st.subheader("Consolidación Histórica de Prestaciones Oncomamarias (2015 - 2025)")
        mostrar_tabla_configurable(tabla_anual_vista, tipo_tabla="consolidacion")
