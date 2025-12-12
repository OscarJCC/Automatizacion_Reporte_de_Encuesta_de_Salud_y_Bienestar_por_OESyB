#!/usr/bin/env python3
"""
Script principal para generación de reportes de encuestas de salud y bienestar.

Este script orquesta todo el proceso de generación de reportes:
1. Carga de datos
2. Procesamiento de datos
3. Generación de visualizaciones
4. Extracción de estadísticas
5. Generación de documento PDF

Uso:
    python main.py
"""

import os
import sys
from datetime import datetime

# Configurar path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imports de módulos propios
from config import settings
from src.utils.text_processing import normalizar_nombre_archivo
from src.utils.file_utils import crear_directorio_salida
from src.data.loader import (
    load_survey_data,
    load_metadata,
    get_universities_list,
    filter_by_university
)
from src.data.processor import (
    process_diseases,
    process_drugs,
    calculate_addiction_risk,
    calculate_psychological_wellbeing,
    calculate_suicide_risk,
    calculate_anxiety_level,
    calculate_depression_level,
    process_municipalities,
    process_gender_by_university
)
from src.visualization.demographics import (
    plot_universities_bar,
    plot_universities_pie,
    plot_gender_bar,
    plot_gender_pie,
    plot_gender_by_university,
    plot_municipalities
)
from src.visualization.health import (
    plot_diseases_count,
    plot_diseases_percentage,
    plot_substance_use
)
from src.visualization.mental_health import (
    plot_addiction_risk,
    plot_psychological_wellbeing_bar,
    plot_psychological_wellbeing_pie,
    plot_suicide_risk,
    plot_anxiety,
    plot_depression
)
from src.report.statistics import (
    extract_demographic_stats,
    extract_health_stats,
    extract_mental_health_stats
)
from src.report.latex_generator import (
    create_document,
    setup_header_footer,
    add_cover_page,
    add_introduction,
    add_executive_summary,
    add_results_section,
    generate_pdf
)


def generate_visualizations(data, carpeta_salida, es_general, df_universidades=None, 
                              df_universidad_sexo=None):
    """
    Genera todas las visualizaciones para un conjunto de datos.
    
    Args:
        data: DataFrame con los datos filtrados
        carpeta_salida: Carpeta donde guardar las gráficas
        es_general: Si es el reporte general
        df_universidades: DataFrame de universidades (solo para reporte general)
        df_universidad_sexo: DataFrame de género por universidad (solo para reporte general)
    """
    print("  Generando visualizaciones demográficas...")
    
    # Gráficas de universidades (solo para reporte general)
    if es_general and df_universidades is not None:
        plot_universities_bar(df_universidades, carpeta_salida)
        plot_universities_pie(df_universidades, carpeta_salida)
    
    # Gráficas de sexo
    df_sexo = data[settings.COL_SEXO].value_counts().sort_values(
        ascending=False
    ).reset_index()
    df_sexo.columns = ["Sexo", "freq"]
    plot_gender_bar(df_sexo, carpeta_salida)
    plot_gender_pie(df_sexo, carpeta_salida)
    
    # Gráficas de género por universidad (solo para reporte general)
    if es_general and df_universidad_sexo is not None:
        plot_gender_by_university(df_universidad_sexo, carpeta_salida)
    
    # Gráficas de municipios
    metadata = load_metadata(settings.RUTA_BASE)
    df_municipio = process_municipalities(data, metadata)
    tiene_muchos_municipios = len(df_municipio) > 19
    plot_municipalities(df_municipio, carpeta_salida, split=tiene_muchos_municipios)
    
    print("  Generando visualizaciones de salud...")
    
    # Gráficas de enfermedades
    df_enfermedades = process_diseases(data)
    plot_diseases_count(df_enfermedades, carpeta_salida)
    plot_diseases_percentage(df_enfermedades, carpeta_salida)
    
    # Gráficas de consumo de sustancias
    df_drogas = process_drugs(data)
    plot_substance_use(df_drogas, carpeta_salida)
    
    print("  Generando visualizaciones de salud mental...")
    
    # Gráficas de riesgo de adicción
    _, _, porc_conteo_cs = calculate_addiction_risk(data)
    plot_addiction_risk(porc_conteo_cs, carpeta_salida)
    
    # Gráficas de bienestar psicológico
    _, conteo_clas_ryff, sizes_ryff = calculate_psychological_wellbeing(data)
    labels_ryff = conteo_clas_ryff.index
    plot_psychological_wellbeing_bar(labels_ryff, sizes_ryff, carpeta_salida)
    plot_psychological_wellbeing_pie(labels_ryff, sizes_ryff, carpeta_salida)
    
    # Gráficas de riesgo de suicidio
    _, conteo_clas_rs, _ = calculate_suicide_risk(data)
    plot_suicide_risk(conteo_clas_rs, carpeta_salida)
    
    # Gráficas de ansiedad
    _, conteo_clas_ans = calculate_anxiety_level(data)
    plot_anxiety(conteo_clas_ans, carpeta_salida)
    
    # Gráficas de depresión
    _, conteo_clas_depr = calculate_depression_level(data)
    plot_depression(conteo_clas_depr, carpeta_salida)
    
    return tiene_muchos_municipios


def generate_report_for_university(data, universidad_nombre, universidad_idx, 
                                     total_universidades, carpeta_reportes,
                                     df_universidades=None,
                                     df_universidad_sexo=None):
    """
    Genera el reporte completo para una universidad.
    
    Args:
        data: DataFrame con los datos filtrados
        universidad_nombre: Nombre de la universidad
        universidad_idx: Índice de la universidad
        total_universidades: Total de universidades
        carpeta_reportes: Carpeta base donde guardar los reportes
        df_universidades: DataFrame de universidades (solo para reporte general)
        df_universidad_sexo: DataFrame de género por universidad (solo para reporte general)
    """
    print(f"\n[{universidad_idx + 1}/{total_universidades}] Procesando: {universidad_nombre}")
    
    es_general = (universidad_nombre == "GENERAL")
    
    # Crear directorio de salida para gráficas
    t_guardado = normalizar_nombre_archivo(universidad_nombre)
    carpeta_salida = crear_directorio_salida(
        carpeta_reportes,
        f"graficas/{t_guardado}"
    )
    
    # Generar visualizaciones
    tiene_muchos_municipios = generate_visualizations(
        data, carpeta_salida, es_general, df_universidades, df_universidad_sexo
    )
    
    print("  Extrayendo estadísticas...")
    
    # Procesar datos para estadísticas
    df_enfermedades = process_diseases(data)
    _, _, porc_conteo_cs = calculate_addiction_risk(data)
    _, conteo_clas_ryff, sizes_ryff = calculate_psychological_wellbeing(data)
    _, conteo_clas_rs, porc_conteo_rs = calculate_suicide_risk(data)
    
    # Extraer estadísticas
    stats_demo = extract_demographic_stats(data)
    stats_health = extract_health_stats(data, df_enfermedades)
    stats_mental = extract_mental_health_stats(
        data, df_enfermedades, porc_conteo_cs, conteo_clas_ryff,
        sizes_ryff, conteo_clas_rs, porc_conteo_rs
    )
    
    print("  Generando documento PDF...")
    
    # Crear documento LaTeX
    doc = create_document()
    setup_header_footer(doc)
    add_cover_page(doc, universidad_nombre, settings.RUTA_BASE, es_general)
    add_introduction(doc, universidad_nombre, es_general)
    add_executive_summary(doc, stats_demo, stats_health, stats_mental)
    add_results_section(
        doc, len(data), universidad_nombre, carpeta_salida,
        es_general, tiene_muchos_municipios
    )
    
    # Generar PDF en carpeta de reportes
    generate_pdf(doc, carpeta_reportes, f"2025-ReporteCoahuila-{t_guardado}")
    
    print(f"  ✓ Reporte generado: reportes/.../2025-ReporteCoahuila-{t_guardado}.pdf")


def main():
    """
    Función principal que ejecuta todo el proceso de generación de reportes.
    """
    print("=" * 80)
    print("SISTEMA DE GENERACIÓN DE REPORTES DE SALUD Y BIENESTAR")
    print("=" * 80)
    
    # Configurar ruta base
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    settings.set_base_path(ruta_base)
    
    print(f"\nRuta base: {ruta_base}")
    
    # Crear carpeta de reportes con fecha
    fecha_actual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    carpeta_reportes = crear_directorio_salida(
        ruta_base,
        f"reportes/{fecha_actual}"
    )
    print(f"Carpeta de reportes: {carpeta_reportes}")
    
    # Cargar datos
    print("\nCargando datos...")
    data_completa = load_survey_data(ruta_base, use_csv=True)
    print(f"  ✓ Datos cargados: {len(data_completa)} registros")
    
    # Obtener lista de universidades
    universidades = get_universities_list(data_completa)
    print(f"  ✓ Universidades encontradas: {len(universidades)}")
    
    # Preparar datos para reporte general
    df_universidades = data_completa[settings.COL_UNIVERSIDAD].value_counts().sort_values(
        ascending=True
    ).reset_index()
    df_universidades.columns = ["Universidad", "freq"]
    
    df_universidad_sexo = process_gender_by_university(data_completa)
    
    # Generar reportes para cada universidad
    print("\n" + "=" * 80)
    print("GENERANDO REPORTES")
    print("=" * 80)
    
    for idx, universidad in enumerate(universidades):
        # Filtrar datos
        data_filtrada = filter_by_university(data_completa, universidad)
        
        # Generar reporte
        if universidad == "GENERAL":
            generate_report_for_university(
                data_filtrada, universidad, idx, len(universidades),
                carpeta_reportes, df_universidades, df_universidad_sexo
            )
        else:
            generate_report_for_university(
                data_filtrada, universidad, idx, len(universidades),
                carpeta_reportes
            )
    
    print("\n" + "=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print(f"\nSe generaron {len(universidades)} reportes exitosamente.")
    print(f"Ubicación: {carpeta_reportes}")


if __name__ == "__main__":
    main()
