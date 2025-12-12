"""
Utilidades para manejo de archivos y directorios.
"""

import os


def generador_ruta_guardado(carpeta, n_archivo, extension=None):
    """
    Genera una ruta completa para guardar un archivo.
    
    Args:
        carpeta (str): Ruta de la carpeta donde guardar
        n_archivo (str): Nombre del archivo (sin extensión)
        extension (str, optional): Extensión del archivo (sin punto). Defaults to None.
        
    Returns:
        str: Ruta completa del archivo
        
    Examples:
        >>> generador_ruta_guardado("/tmp", "reporte", "pdf")
        '/tmp/reporte.pdf'
        >>> generador_ruta_guardado("/tmp", "reporte.pdf")
        '/tmp/reporte.pdf'
    """
    if extension:
        archivo = f"{n_archivo}.{extension}"
    else:
        archivo = n_archivo
    
    return os.path.join(carpeta, archivo)


def crear_directorio_salida(ruta_base, nombre_carpeta):
    """
    Crea un directorio de salida si no existe.
    
    Args:
        ruta_base (str): Ruta base donde crear el directorio
        nombre_carpeta (str): Nombre del directorio a crear
        
    Returns:
        str: Ruta completa del directorio creado
    """
    carpeta_salida = os.path.join(ruta_base, nombre_carpeta)
    os.makedirs(carpeta_salida, exist_ok=True)
    return carpeta_salida
