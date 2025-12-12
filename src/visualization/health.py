"""
Módulo de visualizaciones de salud física.
Contiene funciones para generar gráficas de enfermedades y consumo de sustancias.
"""

import matplotlib.pyplot as plt
import pandas as pd
from config import settings
from src.utils.file_utils import generador_ruta_guardado


def plot_diseases_count(df_enfermedades, carpeta_salida):
    """
    Genera gráfica de barras horizontales con cantidad de enfermedades.
    
    Args:
        df_enfermedades (pd.DataFrame): DataFrame con columnas 'Enfermedad', 'Cantidad', 'Porcentaje'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=(18, 5))
    
    # Excluir "Ninguna"
    sizes = df_enfermedades["Cantidad"][1:]
    labels = df_enfermedades["Enfermedad"][1:]
    
    bars = ax.barh(labels, sizes, color=settings.COLORS)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5,
            bar.get_y() + bar.get_height()/2,
            f"{int(width)}",
            va="center"
        )
        ax.text(
            -0.1, 0,
            f"Ninguna: {df_enfermedades['Cantidad'].iloc[0]}",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )
    
    ax.invert_yaxis()
    ax.tick_params(axis="y", labelsize=13)
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Enfermedades_Barras_1", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_diseases_percentage(df_enfermedades, carpeta_salida):
    """
    Genera gráfica de barras horizontales con porcentaje de enfermedades.
    
    Args:
        df_enfermedades (pd.DataFrame): DataFrame con columnas 'Enfermedad', 'Cantidad', 'Porcentaje'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=(18, 5))
    
    # Excluir "Ninguna"
    porc = df_enfermedades["Porcentaje"][1:]
    labels = df_enfermedades["Enfermedad"][1:]
    
    bars = ax.barh(labels, porc, color=settings.COLORS)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 0.5,
            bar.get_y() + bar.get_height()/2,
            f"{width:.2f}%",
            va="center"
        )
        ax.text(
            1.1, 0,
            f"Ninguna: {df_enfermedades['Porcentaje'].iloc[0]:.2f}%",
            transform=ax.transAxes,
            ha="center",
            va="center",
            fontsize=11,
            fontweight="bold"
        )
    
    ax.invert_xaxis()
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    ax.tick_params(axis="y", labelsize=13)
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Enfermedades_Barras_2", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_substance_use(df_drogas, carpeta_salida):
    """
    Genera gráfica de barras de consumo de sustancias.
    
    Args:
        df_drogas (pd.DataFrame): DataFrame con columnas 'Droga' y 'Cantidad'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    
    sizes = df_drogas["Cantidad"]
    labels = df_drogas["Droga"]
    
    bars = ax.bar(labels, sizes, color=settings.COLORS)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f"{height}",
            ha="center", va="bottom",
        )
    
    ax.tick_params(axis='x', labelrotation=90)
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Consumo_Sustancias", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()
