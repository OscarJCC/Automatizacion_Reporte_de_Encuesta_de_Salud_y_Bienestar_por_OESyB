"""
Módulo para procesamiento y transformación de datos de encuestas.
"""

import pandas as pd
import numpy as np
from config import settings
from src.utils.text_processing import (
    split_enfermedades, 
    ajusta_datos_drogas, 
    contiene_sustancia
)


def process_diseases(data):
    """
    Procesa los datos de enfermedades, separando y contando cada una.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        pd.DataFrame: DataFrame con enfermedades procesadas y sus frecuencias
    """
    df_enfermedades = data[settings.COL_ENFERMEDADES].value_counts().sort_values(
        ascending=False
    ).reset_index()
    df_enfermedades.columns = ["Enfermedad", "Cantidad"]
    
    # Separar enfermedades que están en la misma celda
    df_enfermedades = df_enfermedades.assign(
        Enfermedad=df_enfermedades["Enfermedad"].apply(split_enfermedades)
    ).explode("Enfermedad")
    
    # Agrupar y sumar
    df_enfermedades = df_enfermedades.groupby("Enfermedad", as_index=False)["Cantidad"].sum()
    df_enfermedades = df_enfermedades.sort_values(by="Cantidad", ascending=False)
    
    # Calcular porcentajes
    df_enfermedades["Porcentaje"] = (
        df_enfermedades["Cantidad"] / df_enfermedades["Cantidad"].sum() * 100
    )
    
    return df_enfermedades


def process_drugs(data):
    """
    Procesa los datos de consumo de sustancias.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        pd.DataFrame: DataFrame con sustancias procesadas y sus frecuencias
    """
    df_drogas = data[settings.COL_CONSUMO_SUSTANCIAS].apply(ajusta_datos_drogas)
    df_drogas = df_drogas[df_drogas != "ninguna"].dropna()
    
    df_us_drogas = df_drogas.apply(
        lambda x: contiene_sustancia(x, settings.LISTA_BUSQUEDA_DROGA)
    ).value_counts().reset_index()
    
    df_us_drogas.columns = ['Droga', 'Cantidad']
    
    # Mapear a categorías estándar
    df_us_drogas['Droga'] = df_us_drogas['Droga'].apply(
        lambda x: settings.MAPA_SUSTANCIAS.get(x, x)
    )
    
    # Agrupar por categoría
    df_us_drogas = df_us_drogas.groupby('Droga')['Cantidad'].sum().reset_index()
    df_us_drogas = df_us_drogas.sort_values('Cantidad', ascending=False)
    
    return df_us_drogas


def calculate_addiction_risk(data):
    """
    Calcula el nivel de riesgo de adicción.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        tuple: (DataFrame con clasificación, conteo por categoría, porcentaje por categoría)
    """
    df_cs = data[settings.LIST_PREG_CS].replace("Opción 4", 0).copy()
    df_cs = df_cs.apply(pd.to_numeric, errors='coerce').fillna(0)
    df_cs_s = df_cs.sum(axis=1)
    df_cs.loc[:, 'sum'] = df_cs_s
    df_cs.loc[:, 'clasificacion'] = pd.cut(
        df_cs_s,
        bins=settings.BINS_ADICCION,
        labels=settings.LABELS_ADICCION
    )
    
    conteo_clas_cs = df_cs["clasificacion"].value_counts().sort_index()
    porc_conteo_cs = conteo_clas_cs / conteo_clas_cs.sum()
    
    return df_cs, conteo_clas_cs, porc_conteo_cs


def calculate_psychological_wellbeing(data):
    """
    Calcula el nivel de bienestar psicológico (escala RYFF).
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        tuple: (DataFrame con clasificación, conteo por categoría, porcentajes)
    """
    df_ryff = data[settings.LIST_PREG_RYFF].copy()
    df_ryff_s = df_ryff.sum(axis=1)
    df_ryff.loc[:, 'sum'] = df_ryff_s
    df_ryff.loc[:, 'clasificacion'] = pd.cut(
        df_ryff_s,
        bins=settings.BINS_RYFF,
        labels=settings.LABELS_RYFF
    )
    
    conteo_clas_ryff = df_ryff["clasificacion"].value_counts().sort_index()
    porc_conteo_ryff = conteo_clas_ryff / conteo_clas_ryff.sum()
    sizes_ryff = porc_conteo_ryff.values * 100
    
    return df_ryff, conteo_clas_ryff, sizes_ryff


def calculate_suicide_risk(data):
    """
    Calcula el riesgo de suicidio.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        tuple: (DataFrame con clasificación, conteo por categoría, porcentajes)
    """
    df_rs = data[settings.LIST_PREG_RS].copy()
    df_rs_s = df_rs.sum(axis=1)
    df_rs.loc[:, 'sum'] = df_rs_s
    df_rs.loc[:, 'clasificacion'] = pd.cut(
        df_rs_s,
        bins=settings.BINS_SUICIDIO,
        labels=settings.LABELS_SUICIDIO
    )
    
    conteo_clas_rs = df_rs["clasificacion"].value_counts().sort_index()
    porc_conteo_rs = conteo_clas_rs / conteo_clas_rs.sum() * 100
    
    return df_rs, conteo_clas_rs, porc_conteo_rs


def calculate_anxiety_level(data):
    """
    Calcula el nivel de ansiedad.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        tuple: (Series con clasificación, conteo por categoría)
    """
    df_ans = data["Ansiedad"].copy()
    clasificacion_ans = pd.cut(
        df_ans,
        bins=settings.BINS_ANSIEDAD,
        labels=settings.LABELS_ANSIEDAD
    )
    conteo_clas_ans = clasificacion_ans.value_counts().sort_index()
    
    return clasificacion_ans, conteo_clas_ans


def calculate_depression_level(data):
    """
    Calcula el nivel de depresión.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        tuple: (Series con clasificación, conteo por categoría)
    """
    df_depr = data["Depresion"].copy()
    clasificacion_depr = pd.cut(
        df_depr,
        bins=settings.BINS_DEPRESION,
        labels=settings.LABELS_DEPRESION
    )
    conteo_clas_depr = clasificacion_depr.value_counts().sort_index()
    
    return clasificacion_depr, conteo_clas_depr


def process_municipalities(data, metadata):
    """
    Procesa los datos de municipios.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        metadata (pd.DataFrame): DataFrame con metadatos
        
    Returns:
        pd.DataFrame: DataFrame con municipios y sus frecuencias
    """
    df_municipio = data[settings.COL_MUNICIPIO].value_counts().sort_values(
        ascending=True
    ).reset_index()
    df_municipio.columns = ["Clave", "freq"]
    
    # Obtener mapeo de claves a nombres
    df_mcm = metadata.iloc[0:38, 6:8].copy()
    df_mcm.columns = ["Municipio", "Clave"]
    
    # Merge y limpieza
    df_us_municipio = df_mcm.merge(df_municipio, on="Clave", how="left")
    df_us_municipio = df_us_municipio.sort_values("freq", ascending=True).dropna()
    
    return df_us_municipio


def process_gender_by_university(data):
    """
    Procesa la distribución de género por universidad.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        pd.DataFrame: DataFrame con género por universidad
    """
    df_us_universidad_sexo = data[[settings.COL_UNIVERSIDAD, settings.COL_SEXO]].copy()
    df_us_universidad_sexo.columns = ["Universidad", "Sexo"]
    df_us_universidad_sexo = df_us_universidad_sexo.groupby(
        ["Universidad", "Sexo"]
    ).size().unstack(fill_value=0)
    
    # Asegurar que todas las columnas existan
    for col in settings.GENEROS:
        if col not in df_us_universidad_sexo.columns:
            df_us_universidad_sexo[col] = 0
    
    df_us_universidad_sexo = df_us_universidad_sexo[settings.GENEROS]
    
    return df_us_universidad_sexo
