"""
Módulo para generación de documentos LaTeX y PDFs.
"""

from pylatex import (
    Document,
    Figure,
    NoEscape,
    Package,
    Foot,
    Head,
    PageStyle,
)
from config import settings
from src.utils.file_utils import generador_ruta_guardado


def create_document():
    """
    Crea un documento LaTeX base con configuración inicial.
    
    Returns:
        Document: Documento LaTeX configurado
    """
    doc = Document(geometry_options=settings.GEOMETRY_OPTIONS)
    
    # Paquetes necesarios
    doc.packages.append(Package("graphicx"))
    doc.packages.append(Package("babel", options="spanish"))
    doc.packages.append(Package("setspace"))
    doc.packages.append(Package("titling"))
    doc.packages.append(Package("ragged2e"))
    doc.packages.append(Package("xcolor"))
    
    return doc


def setup_header_footer(doc):
    """
    Configura encabezados y pies de página del documento.
    
    Args:
        doc (Document): Documento LaTeX
    """
    header = PageStyle("header")
    
    # HEADERS
    with header.create(Head("C")):
        header.append(settings.DOC_HEADER_CENTER)
    
    with header.create(Head("R")):
        header.append(NoEscape(r"\rightmark"))
    
    # FOOTERS
    with header.create(Foot("C")):
        header.append(settings.DOC_DATE)
    
    with header.create(Foot("L")):
        header.append(settings.DOC_FOOTER_LEFT)
    
    with header.create(Foot("R")):
        header.append(NoEscape(r"\thepage"))
    
    # Attach style
    doc.preamble.append(NoEscape(r"\spanishdecimal{.}"))
    doc.preamble.append(NoEscape(r"\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}"))
    header.append(NoEscape(r"\renewcommand{\headrulewidth}{0.4pt}"))
    doc.preamble.append(header)
    doc.change_document_style("header")


def add_cover_page(doc, universidad_nombre, ruta_base, es_general=False):
    """
    Agrega la portada al documento.
    
    Args:
        doc (Document): Documento LaTeX
        universidad_nombre (str): Nombre de la universidad
        ruta_base (str): Ruta base del proyecto para encontrar logos
        es_general (bool): Si es el reporte general
    """
    doc.append(NoEscape(r"\thispagestyle{empty}"))
    
    # Rutas absolutas para logos
    import os
    logo_im_path = os.path.join(ruta_base, "Logos", "LogosIM.pdf")
    
    if es_general:
        text_port = f"{universidad_nombre}ES"
        logo_inst = r"\vspace{1.7cm}"
    else:
        text_port = universidad_nombre
        logo_universidad_path = os.path.join(ruta_base, "Logos", f"Logo-{text_port}.pdf")
        logo_inst = fr"""\begin{{figure}}[htbp]%
            \centering
            \includegraphics[height=2.5cm]{{{logo_universidad_path}}}%
        \end{{figure}}"""
    
    # Formatear listas de autores
    elaboro_str = "\\\\\n".join([f"\\textbf{{{autor}}}" for autor in settings.ELABORO])
    presenta_str = "\\\\ ".join([f"\\textbf{{{autor}}}" for autor in settings.PRESENTA])
    
    doc.append(NoEscape(fr"""
    \begin{{center}}
        \begin{{figure}}[htbp]%
            \centering
            \includegraphics[width=\textwidth]{{{logo_im_path}}}%
        \end{{figure}}
        
        \vspace{{0.7cm}}
        \LARGE
        {settings.DOC_INSTITUTION}
        
        \vspace{{0.7cm}}
        \LARGE
        {settings.DOC_OBSERVATORY}
        
        \vspace{{0.8cm}}	
        \Large
        \textbf{{{settings.DOC_TITLE}}}

        \vspace{{0.3cm}}	
        \Large
        {text_port}
        {logo_inst}
        
        \vspace{{0.8cm}}
        \normalsize	
        ELABORÓ \\
        \vspace{{.3cm}}
        {elaboro_str}
        
        \vspace{{0.8cm}}
        \normalsize	
        PRESENTA \\
        \vspace{{.3cm}}
        {presenta_str}
        
        \vspace{{1.3cm}}
        \today
    \end{{center}}

    \newpage
    \tableofcontents
    \newpage
    """))


def add_introduction(doc, universidad_nombre, es_general=False):
    """
    Agrega la sección de introducción al documento.
    
    Args:
        doc (Document): Documento LaTeX
        universidad_nombre (str): Nombre de la universidad
        es_general (bool): Si es el reporte general
    """
    if es_general:
        text_ref = f"correspondientes al nivel {universidad_nombre}"
    else:
        text_ref = f"correspondientes a {universidad_nombre}"
    
    doc.append(NoEscape(rf"""
    \section{{INTRODUCCIÓN}}\label{{sec:int}}

        La salud mental y el bienestar de los estudiantes universitarios han cobrado una relevancia creciente en el ámbito académico y de salud pública, debido a la identificación de múltiples factores que pueden afectar su desempeño y calidad de vida. La Encuesta de Salud y Bienestar aplicada a los estudiantes de educación superior en 2025 reveló una alta prevalencia de trastornos como ansiedad y depresión, así como un considerable consumo de alcohol y tabaco en los universitarios de las unidades Saltillo, Torreón y Norte. Estos hallazgos subrayan la necesidad de evaluar de manera continua la salud de la comunidad estudiantil, a fin de generar estrategias preventivas y promover intervenciones oportunas.

        Los primeros años universitarios son una etapa de importantes transiciones y desafíos, en la que los estudiantes deben adaptarse a nuevas exigencias académicas, sociales y económicas. Estas condiciones pueden incrementar el riesgo de desarrollar problemas de salud mental, particularmente en jóvenes que enfrentan condiciones socioeconómicas adversas o que carecen de redes de apoyo. De acuerdo con estudios recientes, la presencia de factores como el estrés financiero, la inseguridad alimentaria y la falta de acceso a servicios de salud pueden exacerbar síntomas de ansiedad y depresión en poblaciones universitarias (González et al., 2023).

        Asimismo, la Organización Mundial de la Salud (OMS, 2023) ha advertido que el consumo de sustancias como alcohol y tabaco sigue siendo un problema latente en este grupo etario, asociado a intentos de regulación emocional y a contextos de socialización poco saludables.

        En este contexto, la Encuesta de Salud y Bienestar del OESyB tiene
        como objetivo actualizar y ampliar el conocimiento sobre el estado de salud de los estudiantes de nuevo ingreso, evaluando no solo aspectos psicológicos como la ansiedad, la depresión y el riesgo suicida, sino también variables económicas, la presencia de enfermedades crónicas y el consumo de sustancias. La inclusión de estos factores permitirá un análisis integral del bienestar estudiantil, favoreciendo la identificación de grupos vulnerables y la implementación de estrategias institucionales más eficaces para el cuidado de su salud.
        
        Finalmente, es importante señalar que el presente resumen se elaboró a partir de los datos {text_ref} de la encuesta, con el fin de ofrecer una visión amplia del estado de salud y bienestar de la población estudiantil evaluada.
    """))


def add_executive_summary(doc, stats_demo, stats_health, stats_mental):
    """
    Agrega el resumen ejecutivo al documento.
    
    Args:
        doc (Document): Documento LaTeX
        stats_demo (dict): Estadísticas demográficas
        stats_health (dict): Estadísticas de salud
        stats_mental (dict): Estadísticas de salud mental
    """
    # Características socioeconómicas
    caracteristicas_socioeconomicas = fr"""
        El análisis de la población estudiantil muestra que los hombres, representando el ${stats_demo['lista_us_sexo_porc'][0]:.2f}\%$, mientras que las mujeres constituyen el ${stats_demo['lista_us_sexo_porc'][1]:.2f}\%$ y el ${stats_demo['lista_us_sexo_porc'][2] if len(stats_demo['lista_us_sexo_porc']) > 2 else 0.0:.2f}\%$ se identifica como intersexual. La edad promedio de los estudiantes es de ${stats_demo['edad_media']}$ años.
        
        En términos de estado civil, se observa que la gran mayoría de los estudiantes son solteros (${stats_demo['mayor_us_estado_civil_porc']:.2f}\%$) y no tienen hijos (${stats_demo['mayor_us_tiene_hijos_porc']:.2f}\%$), lo que refleja que se trata, en su mayoría, de una población joven y en etapa de formación académica.

        Respecto a la situación laboral, el ${stats_demo['us_si_trabaja_porc']:.2f}\%$ e los estudiantes se encuentra trabajando. De este grupo, más de la mitad (${stats_demo['us_trabaja_jornada_comp']:.2f}\%$) realiza una jornada laboral de tiempo completo, mientras que el resto cumple con jornadas parciales o flexibles.
        
        En lo referente al ingreso familiar, la mayoría de los estudiantes (${stats_demo['us_ingreso_familiar_men_20000']:.2f}\%$) proviene de hogares cuyos ingresos mensuales son iguales o inferiores a \$20000 pesos, lo que indica que gran parte de la población estudiantil pertenece a familias con ingresos medios y bajos.
        
        Finalmente, se destaca que el ${stats_demo['us_beca']:.2f}\%$ de los estudiantes ha recibido algún tipo de beca durante su formación académica, lo que evidencia la importancia de los apoyos económicos para facilitar la continuidad educativa y el acceso a oportunidades de estudio.
    """
    
    # Características de salud física
    caracterisitcas_salud_fisica = fr"""
        Del total de estudiantes encuestados, ${stats_health['us_enfermos']:.0f}$ reportaron tener alguna enfermedad crónica, lo que representa el ${stats_health['us_enfermos_porc']:.2f}\%$ de la población estudiantil. En cuanto a la prevalencia de enfermedades específicas, la más mencionada fue {stats_health['mas_enfer_men'][1]} ($n = {stats_health['mas_enfer_us'][1]:.0f}$), seguida por {stats_health['mas_enfer_men'][4]} ($n = {stats_health['mas_enfer_us'][4]:.0f}$). Esta información permite identificar las condiciones de salud más frecuentes entre los estudiantes y orientar acciones preventivas y de atención médica.
        
        Respecto a los hábitos de sueño, casi la mitad de los estudiantes (${stats_health['us_sueño_max']:.2f}\%$) reporta dormir entre {stats_health['us_sueño_n']} al día, lo que se encuentra dentro de los rangos recomendados para mantener un adecuado bienestar físico y cognitivo.
        
        Finalmente, en lo relativo a la actividad física, ${stats_health['us_deporte']:.2f}\%$ de los estudiantes practica algún deporte al menos 1-2 veces por semana, lo que refleja un nivel moderado de actividad física dentro de la población estudiantil.
    """
    
    # Riesgo de adicción
    riesgo_adiccion = (
        "no se registraron casos en la categoría de riesgo alto, lo que sugiere que no se identificaron individuos con un nivel crítico de riesgo."
        if stats_mental['us_cs'][2] == 0
        else f"se registró un ${stats_mental['us_cs'][2]:.2f}\\%$ de casos en la categoría de riesgo alto, lo que sugiere que existe un grupo que requiere especial atención."
    )
    
    # Características de salud mental
    partes_droga_str = ", ".join(stats_mental['partes_droga'][:-1]) + " y " + stats_mental['partes_droga'][-1] if len(stats_mental['partes_droga']) > 1 else stats_mental['partes_droga'][0]
    
    caracteristicas_salud_mental = rf"""
    En relación con la salud mental, se identificó que un total de {stats_mental['us_salud_menta_bad'][1]:.0f} estudiantes reportaron presentar {stats_mental['us_salud_menta_bad'][0]}, lo que corresponde al {stats_mental['us_salud_menta_bad'][2]:.2f}\% de toda la población estudiantil encuestada.

    En cuanto al consumo de sustancias, el {stats_mental['us_cons_drogas_porc']:.2f}\% de estudiantes (n = {stats_mental['us_cons_drogas']}) indicó consumir alguna droga. Dentro de este grupo, las sustancias más reportadas fueron {partes_droga_str}.

    Respecto al nivel de riesgo de adicción: {riesgo_adiccion}

    En cuanto al bienestar psicológico, los resultados muestran que {stats_mental['us_ryff'][0]} estudiantes ({stats_mental['us_ryff_por'][0]:.2f}\%) se encuentran en el nivel bajo. Por otro lado, {stats_mental['us_ryff'][1]} estudiantes ({stats_mental['us_ryff_por'][1]:.2f}\%) se sitúan en un nivel moderado de bienestar. Finalmente, {stats_mental['us_ryff'][2]} estudiantes ({stats_mental['us_ryff_por'][2]:.2f}\%) muestran un nivel alto de bienestar psicológico.

    En cuanto al riesgo suicida, se encontró que 
    \begin{{center}}
        {{\color{{red}}\fontsize{{20}}{{36}}\selectfont \textbf{{{stats_mental['us_rs'][1]} estudiantes ({stats_mental['us_rs_por'][1]:.2f}\%)}}}}
    \end{{center}}
    presentan un nivel de riesgo significativo, representando una proporción destacable dentro de la población estudiantil evaluada.
    """
    
    doc.append(NoEscape(fr"""
    \section{{RESUMEN EJECUTIVO}}\label{{sec:res_ejec}}
        \subsection{{Características socioeconómicas}}
            {caracteristicas_socioeconomicas}
        
        \subsection{{Características de salud física}}
            {caracterisitcas_salud_fisica}

        \subsection{{Características de salud mental}}
            {caracteristicas_salud_mental}

    """))


def add_results_section(doc, data_length, universidad_nombre, carpeta_salida, 
                         es_general=False, tiene_muchos_municipios=False):
    """
    Agrega la sección de resultados con todas las gráficas.
    
    Args:
        doc (Document): Documento LaTeX
        data_length (int): Número de estudiantes en la muestra
        universidad_nombre (str): Nombre de la universidad
        carpeta_salida (str): Carpeta donde están las gráficas
        es_general (bool): Si es el reporte general
        tiene_muchos_municipios (bool): Si hay más de 19 municipios
    """
    if es_general:
        text_ref = f"correspondientes al nivel {universidad_nombre}"
    else:
        text_ref = f"correspondientes a {universidad_nombre}"
    
    doc.append(NoEscape(fr"""
    \section{{RESULTADOS}}\label{{sec:pob}}

    En cuanto a la composición de la muestra, los datos incluyen información proporcionada por {data_length} estudiantes {text_ref}, lo que permite analizar las condiciones de salud, el bienestar y los factores asociados, garantizando que los resultados reflejen las características del grupo evaluado.

    """))
    
    # Gráficas de universidades (solo para reporte general)
    if es_general:
        with doc.create(Figure(position="htbp")) as plot:
            plot.append(NoEscape(r"""
                \subsection{Porcentaje de usuarios por institución}
                \vspace{-0.5em}
            """))
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Barras", "pdf"),
                width=NoEscape(r"\linewidth")
            )
            plot.append(NoEscape(r"\vspace{-0.5em}"))
        
        with doc.create(Figure(position="htbp")) as plot:
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Circulo", "pdf"),
                width=NoEscape(r"\linewidth")
            )
            plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de sexo
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por sexo}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Sexo_Barras", "pdf"),
            width=NoEscape(r"0.5\linewidth")
        )
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Sexo_Circulo", "pdf"),
            width=NoEscape(r"0.5\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
        plot.append(NoEscape(r"\par"))
        if es_general:
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Sexo", "pdf"),
                width=NoEscape(r"\linewidth")
            )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de municipios
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por municipio}
            \vspace{-0.5em}
        """))
        if tiene_muchos_municipios:
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras_1", "pdf"),
                width=NoEscape(r"0.5\linewidth")
            )
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras_2", "pdf"),
                width=NoEscape(r"0.5\linewidth")
            )
        else:
            plot.add_image(
                generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras", "pdf"),
                width=NoEscape(r"0.5\linewidth")
            )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de enfermedades
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por enfermedad}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Enfermedades_Barras_1", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
        plot.append(NoEscape(r"\par"))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Enfermedades_Barras_2", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de consumo de sustancias
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por consumo de sustancias}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Consumo_Sustancias", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de riesgo de adicción
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por nivel de riesgo de adicción}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Riesgo_Adiccion", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de bienestar psicológico
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por grado de bienestar psicológico}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Bienestar_Psicologico_Circulo", "pdf"),
            width=NoEscape(r"0.5\linewidth")
        )
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Bienestar_Psicologico_Barras", "pdf"),
            width=NoEscape(r"0.5\linewidth")
        )
    
    # Gráficas de riesgo de suicidio
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por riesgo de sucidio}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Riesgo_Suicidio", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de ansiedad
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por estado de ansiedad}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Estado_Ansiedad", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))
    
    # Gráficas de depresión
    with doc.create(Figure(position="htbp")) as plot:
        plot.append(NoEscape(r"""
            \subsection{Porcentaje de usuarios por estado de depresión}
            \vspace{-0.5em}
        """))
        plot.add_image(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Estado_Depresion", "pdf"),
            width=NoEscape(r"\linewidth")
        )
        plot.append(NoEscape(r"\vspace{-0.5em}"))


def generate_pdf(doc, ruta_base, nombre_archivo):
    """
    Genera el PDF final del documento.
    
    Args:
        doc (Document): Documento LaTeX completo
        ruta_base (str): Ruta base donde guardar
        nombre_archivo (str): Nombre del archivo (sin extensión)
    """
    doc.generate_pdf(
        generador_ruta_guardado(ruta_base, nombre_archivo),
        clean_tex=False
    )
