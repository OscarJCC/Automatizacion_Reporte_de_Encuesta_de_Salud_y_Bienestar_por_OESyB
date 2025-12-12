"""
Módulo para carga de datos desde archivos Excel y CSV.
"""

import pandas as pd
import os
from config import settings


def load_survey_data(ruta_base, use_csv=True):
    """
    Carga los datos de la encuesta desde archivo CSV o Excel.
    
    Args:
        ruta_base (str): Ruta base donde se encuentran los archivos
        use_csv (bool): Si True, carga desde CSV. Si False, desde Excel.
        
    Returns:
        pd.DataFrame: DataFrame con los datos de la encuesta
    """
    if use_csv:
        file_path = os.path.join(ruta_base, settings.DATA_FILE_CSV)
        return pd.read_csv(file_path)
    else:
        file_path = os.path.join(ruta_base, settings.DATA_FILE_EXCEL)
        return pd.read_excel(file_path, sheet_name="Hoja1")


def load_metadata(ruta_base):
    """
    Carga los metadatos (notas) desde el archivo Excel.
    
    Args:
        ruta_base (str): Ruta base donde se encuentran los archivos
        
    Returns:
        pd.DataFrame: DataFrame con los metadatos
    """
    file_path = os.path.join(ruta_base, settings.DATA_FILE_EXCEL)
    return pd.read_excel(file_path, sheet_name=settings.METADATA_SHEET)


def get_universities_list(data):
    """
    Obtiene la lista de universidades presentes en los datos.
    
    Args:
        data (pd.DataFrame): DataFrame con los datos de la encuesta
        
    Returns:
        list: Lista de universidades, comenzando con "GENERAL"
    """
    universidades = ["GENERAL"]
    df_universidades = data[settings.COL_UNIVERSIDAD].value_counts().sort_values(
        ascending=False
    ).reset_index()
    universidades += list(df_universidades[settings.COL_UNIVERSIDAD])
    return universidades


def filter_by_university(data, universidad_nombre):
    """
    Filtra los datos por universidad.
    
    Args:
        data (pd.DataFrame): DataFrame con todos los datos
        universidad_nombre (str): Nombre de la universidad. Si es "GENERAL", retorna todos los datos.
        
    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    if universidad_nombre == "GENERAL":
        return data.copy()
    else:
        return data[data[settings.COL_UNIVERSIDAD] == universidad_nombre].copy()
