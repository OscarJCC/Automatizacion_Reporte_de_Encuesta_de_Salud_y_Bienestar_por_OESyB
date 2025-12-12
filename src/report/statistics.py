"""
Módulo para extracción de estadísticas para el reporte.
"""

import pandas as pd
from config import settings
from src.data.processor import process_drugs
from src.utils.text_processing import contiene_sustancia


def extract_demographic_stats(data):
    """
    Extrae estadísticas demográficas.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        dict: Diccionario con estadísticas demográficas
    """
    stats = {}
    
    # Sexo
    df_us_sexo_porc = data[settings.COL_SEXO].value_counts().sort_values(ascending=False)
    stats['lista_us_sexo_porc'] = (df_us_sexo_porc / df_us_sexo_porc.sum() * 100).tolist()
    
    # Edad
    stats['edad_media'] = int(data[settings.COL_EDAD].mean())
    
    # Estado Civil
    df_us_estado_civil_porc = data["Estado civil"].value_counts().sort_values(ascending=True)
    stats['mayor_us_estado_civil_porc'] = max(
        (df_us_estado_civil_porc / df_us_estado_civil_porc.sum() * 100).tolist()
    )
    
    # Hijos
    df_us_tiene_hijos_porc = data["¿Tienes Hijos?"].value_counts().sort_values(ascending=True)
    stats['mayor_us_tiene_hijos_porc'] = max(
        (df_us_tiene_hijos_porc / df_us_tiene_hijos_porc.sum() * 100).tolist()
    )
    
    # Trabajo
    df_us_trabaja_porc = data["Trabajas actualmente"].value_counts().sort_values(ascending=True)
    df_us_trabaja_porc = df_us_trabaja_porc / df_us_trabaja_porc.sum() * 100
    us_si_trabaja_porc = 0
    for i in df_us_trabaja_porc.index:
        if i != "No":
            us_si_trabaja_porc += float(df_us_trabaja_porc[i])
    stats['us_si_trabaja_porc'] = us_si_trabaja_porc
    
    # Jornada Laboral
    df_trabajo = data["Trabajas actualmente"]
    df_us_jornada = data["Tu jornada laboral es de:"]
    df_us_trabaja_si_porc = data[df_trabajo != "No"]
    df_us_jornada_porc = df_us_jornada[df_us_trabaja_si_porc.index].value_counts().sort_values(
        ascending=False
    )
    stats['us_trabaja_jornada_comp'] = (
        df_us_jornada_porc / df_us_jornada_porc.sum() * 100
    ).tolist()[0]
    
    # Ingreso Familiar
    df_us_ingreso_familiar = data[["Ingreso mensual familiar:"]].value_counts().sort_values(
        ascending=True
    )
    df_us_ingreso_familiar = df_us_ingreso_familiar / df_us_ingreso_familiar.sum() * 100
    stats['us_ingreso_familiar_men_20000'] = float(df_us_ingreso_familiar.iloc[2:].sum())
    
    # Beca
    df_us_beca_proc = data[
        "¿Has recibido alguna beca federal, estatal o municipal durante tu trayectoria académica? Especifique el nivel"
    ].value_counts().sort_values(ascending=True)
    df_us_beca_proc = (df_us_beca_proc / df_us_beca_proc.sum() * 100)
    us_beca = 0
    for i in df_us_beca_proc.index:
        if i != "No":
            us_beca += float(df_us_beca_proc[i])
    stats['us_beca'] = us_beca
    
    return stats


def extract_health_stats(data, df_enfermedades):
    """
    Extrae estadísticas de salud física.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        df_enfermedades (pd.DataFrame): DataFrame procesado de enfermedades
        
    Returns:
        dict: Diccionario con estadísticas de salud
    """
    stats = {}
    
    # Enfermedades
    stats['mas_enfer_men'] = df_enfermedades.nlargest(6, 'Cantidad')['Enfermedad'].tolist()
    stats['mas_enfer_us'] = df_enfermedades.nlargest(6, 'Cantidad')['Cantidad'].tolist()
    stats['mas_enfer_us_porc'] = df_enfermedades.nlargest(6, 'Cantidad')['Porcentaje'].tolist()
    
    us_enfermos = 0
    us_enfermos_porc = 0
    for i in range(len(df_enfermedades['Enfermedad'])):
        if df_enfermedades['Enfermedad'].iloc[i] != "Ninguna":
            us_enfermos += int(df_enfermedades['Cantidad'].iloc[i])
            us_enfermos_porc += float(df_enfermedades['Porcentaje'].iloc[i])
    
    stats['us_enfermos'] = us_enfermos
    stats['us_enfermos_porc'] = us_enfermos_porc
    
    # Horas de sueño
    df_us_horas_sueño = data["¿Cuántas horas de sueño tiene al día?"].value_counts().sort_values(
        ascending=True
    )
    df_us_horas_sueño = df_us_horas_sueño / df_us_horas_sueño.sum() * 100
    
    stats['us_sueño_n'] = df_us_horas_sueño.idxmax()
    stats['us_sueño_max'] = df_us_horas_sueño[stats['us_sueño_n']]
    
    # Deporte
    df_us_deporte = data[
        "¿Con qué frecuencia practica algún deporte a la semana?"
    ].value_counts().sort_values(ascending=True)
    df_us_deporte = df_us_deporte / df_us_deporte.sum() * 100
    
    us_deporte = 0
    for i in df_us_deporte.index:
        if i != "No practico":
            us_deporte += df_us_deporte[i]
    stats['us_deporte'] = us_deporte
    
    return stats


def extract_mental_health_stats(data, df_enfermedades, porc_conteo_cs, conteo_clas_ryff, 
                                  sizes_ryff, conteo_clas_rs, porc_conteo_rs):
    """
    Extrae estadísticas de salud mental.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        df_enfermedades (pd.DataFrame): DataFrame procesado de enfermedades
        porc_conteo_cs: Porcentajes de riesgo de adicción
        conteo_clas_ryff: Conteo de bienestar psicológico
        sizes_ryff: Porcentajes de bienestar psicológico
        conteo_clas_rs: Conteo de riesgo suicida
        porc_conteo_rs: Porcentajes de riesgo suicida
        
    Returns:
        dict: Diccionario con estadísticas de salud mental
    """
    stats = {}
    
    # Salud Mental
    var_salud_mental = "Desordenes psiquiátricos (depresión, ansiedad, trastornos de la personalidad, etc.)"
    stats['us_salud_menta_bad'] = df_enfermedades[
        df_enfermedades["Enfermedad"] == var_salud_mental
    ].iloc[0].tolist()
    
    # Drogas
    df_us_drogas = process_drugs(data)
    
    stats['us_cons_drogas'] = df_us_drogas['Cantidad'].sum()
    stats['us_cons_drogas_porc'] = stats['us_cons_drogas'] / len(data) * 100
    stats['droga_mas_cons_us'] = df_us_drogas['Droga'].tolist()[0:4]
    stats['droga_mas_cons_us_c'] = df_us_drogas['Cantidad'].tolist()[0:4]
    stats['partes_droga'] = [
        f"{droga} ($n={cant:.0f}$)" 
        for droga, cant in zip(stats['droga_mas_cons_us'], stats['droga_mas_cons_us_c'])
    ]
    
    # Nivel de riesgo de adicciones
    stats['us_cs'] = porc_conteo_cs.values.tolist()
    
    # Grado de bienestar psicológico
    stats['us_ryff'] = conteo_clas_ryff.values
    stats['us_ryff_por'] = sizes_ryff.tolist()
    
    # Riesgo Suicida
    stats['us_rs'] = conteo_clas_rs.values.tolist()
    stats['us_rs_por'] = porc_conteo_rs.values.tolist()
    
    return stats
