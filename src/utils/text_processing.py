"""
Funciones de procesamiento de texto para normalización y limpieza de datos.
"""

import re
import unicodedata
import pandas as pd
import numpy as np


def split_enfermedades(texto):
    """
    Separa una cadena de enfermedades en una lista.
    
    Utiliza una expresión regular para separar en comas que no estén dentro de paréntesis.
    
    Args:
        texto (str): Texto con enfermedades separadas por comas
        
    Returns:
        list: Lista de enfermedades
    """
    # Expresión regular: separa en comas que no estén dentro de paréntesis
    return re.split(r",\s*(?![^(]*\))", texto)


def ajusta_datos_drogas(x):
    """
    Normaliza y limpia datos de consumo de sustancias.
    
    Realiza las siguientes operaciones:
    - Elimina acentos
    - Convierte a minúsculas
    - Elimina espacios extra
    - Elimina puntuación
    - Normaliza respuestas comunes
    
    Args:
        x: Valor a normalizar (puede ser string, float, NaN)
        
    Returns:
        str or list or np.nan: Texto normalizado, lista de sustancias, o NaN
    """
    if pd.isna(x):
        return np.nan
    
    x = str(x)

    # Quitar acentos
    x = ''.join(
        c for c in unicodedata.normalize('NFKD', x)
        if not unicodedata.combining(c)
    )

    # Minúsculas
    x = x.lower()

    # Quitar espacios extra
    x = x.strip()
    x = " ".join(x.split())

    # Quitar puntos, comas y cualquier caracter raro
    x = re.sub(r"[.,;:!?\-/]", "", x)

    # Correcciones comunes
    if x in ["niguna", "ninguna", "ninguna ", "nada"]:
        return "ninguna"

    if pd.isna(x):
        return []

    return [p.strip() for p in x.split(" y ")]


def contiene_sustancia(texto, lista):
    """
    Busca si el texto contiene alguna sustancia de la lista.
    
    Args:
        texto: Texto donde buscar (puede ser None, float, string)
        lista (list): Lista de sustancias a buscar
        
    Returns:
        str or None: Primera sustancia encontrada o None
    """
    # Si es NaN -> None
    if texto is None or (isinstance(texto, float) and pd.isna(texto)):
        return None

    # Convertir todo a string para evitar arrays o listas
    texto = str(texto)

    # Buscar sustancia
    for sustancia in lista:
        if sustancia in texto:
            return sustancia

    return None


def normalizar_nombre_archivo(texto):
    """
    Normaliza un texto para usarlo como nombre de archivo.
    
    Elimina acentos y reemplaza espacios por guiones bajos.
    
    Args:
        texto (str): Texto a normalizar
        
    Returns:
        str: Texto normalizado para nombre de archivo
    """
    return "".join([
        c for c in unicodedata.normalize("NFKD", texto) 
        if not unicodedata.combining(c)
    ]).replace(" ", "_")
