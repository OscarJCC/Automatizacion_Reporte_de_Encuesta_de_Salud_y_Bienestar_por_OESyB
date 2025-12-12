"""
Módulo de visualizaciones demográficas.
Contiene funciones para generar gráficas de universidades, género y municipios.
"""

import matplotlib.pyplot as plt
import numpy as np
from config import settings
from src.utils.file_utils import generador_ruta_guardado


def plot_universities_bar(df_universidades, carpeta_salida):
    """
    Genera gráfica de barras horizontales de universidades.
    
    Args:
        df_universidades (pd.DataFrame): DataFrame con columnas 'Universidad' y 'freq'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_BARRAS_H)
    
    sizes = df_universidades["freq"]
    labels = df_universidades["Universidad"]
    
    bars = ax.barh(labels, sizes, color=settings.COLORS)
    
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width * 0.5,
            bar.get_y() + bar.get_height()/2,
            f"{int(width)}",
            va="center",
            ha="center",
            color="white",
            fontsize=10
        )
    
    ax.tick_params(axis="y", labelsize=8)
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Barras", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_universities_pie(df_universidades, carpeta_salida):
    """
    Genera gráfica de pastel de universidades.
    
    Args:
        df_universidades (pd.DataFrame): DataFrame con columnas 'Universidad' y 'freq'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_CIRCULO_GRANDE)
    
    ax.set_aspect("equal")
    
    sizes = df_universidades["freq"]
    labels = df_universidades["Universidad"]
    
    wedges, _ = ax.pie(
        sizes,
        labels=None,
        colors=settings.COLORS,
        startangle=90,
        wedgeprops=dict(width=.6)
    )
    
    for i, w in enumerate(wedges):
        ang = (w.theta2 + w.theta1) / 2
        x = np.cos(np.deg2rad(ang)) * 0.65
        y = np.sin(np.deg2rad(ang)) * 0.65
        
        rot = ang
        if 90 < ang < 270:
            rot = ang + 180
        
        ax.text(
            x, y,
            f"{sizes.iloc[i]}",
            ha="center",
            va="center",
            fontsize=13,
            color="white",
            rotation=rot,
        )
    
    ax.legend(
        wedges,
        labels,
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        fontsize=15
    )
    
    plt.subplots_adjust(top=0.92, bottom=0.05)
    plt.tight_layout(pad=0)
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Circulo", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_gender_bar(df_sexo, carpeta_salida):
    """
    Genera gráfica de barras de distribución por género.
    
    Args:
        df_sexo (pd.DataFrame): DataFrame con columnas 'Sexo' y 'freq'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_BARRAS_V)
    
    sizes = df_sexo["freq"]
    labels = df_sexo["Sexo"]
    
    bars = ax.bar(labels, sizes, color=settings.COLORS[-3:])
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f"{height / sizes.sum() * 100:.2f}%",
            ha="center", va="bottom",
            fontsize=11
        )
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Sexo_Barras", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_gender_pie(df_sexo, carpeta_salida):
    """
    Genera gráfica de pastel de distribución por género.
    
    Args:
        df_sexo (pd.DataFrame): DataFrame con columnas 'Sexo' y 'freq'
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_CIRCULO)
    
    sizes = df_sexo["freq"]
    labels = df_sexo["Sexo"]
    
    wedges, _ = ax.pie(
        sizes,
        labels=None,
        colors=settings.COLORS[-3:],
        startangle=90,
        wedgeprops=dict(width=.6)
    )
    
    for i, w in enumerate(wedges):
        ang = (w.theta2 + w.theta1) / 2
        x = np.cos(np.deg2rad(ang)) * 0.65
        y = np.sin(np.deg2rad(ang)) * 0.65
        
        rot = ang
        if 90 < ang < 270:
            rot = ang + 180
        
        ax.text(
            x, y,
            f"{sizes.iloc[i] / sizes.sum() * 100:.2f}%",
            ha="center",
            va="center",
            fontsize=15,
            color="white",
            rotation=rot,
        )
    
    ax.legend(
        wedges,
        labels,
        title="Sexo",
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=11
    )
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Sexo_Circulo", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_gender_by_university(df_universidad_sexo, carpeta_salida):
    """
    Genera gráficas de género por universidad (3 paneles).
    
    Args:
        df_universidad_sexo (pd.DataFrame): DataFrame con género por universidad
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)
    
    for ax, genero, color in zip(axes, settings.GENEROS, settings.COLORS[-3:]):
        df_sexo = df_universidad_sexo[genero].sort_values(ascending=True)
        bars = ax.barh(df_sexo.index, df_sexo.values, alpha=0.8, color=color)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(
                width + max(df_sexo.values)*0.01,
                bar.get_y() + bar.get_height()/2,
                f"{int(width)}",
                va="center",
                fontsize=10
            )
            
            ax.text(
                0.5, -0.12,
                f"Total: {df_sexo.sum()}",
                transform=ax.transAxes,
                ha="center",
                va="center",
                fontsize=11,
                fontweight="bold"
            )
        
        ax.tick_params(axis="y", labelsize=11)
        ax.set_title(genero)
        xmax = df_universidad_sexo[settings.GENEROS].values.max()
        ax.set_xlim(0, xmax * 1.15)
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Universidades_Sexo", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_municipalities(df_municipio, carpeta_salida, split=False):
    """
    Genera gráfica(s) de barras de municipios.
    
    Args:
        df_municipio (pd.DataFrame): DataFrame con columnas 'Municipio' y 'freq'
        carpeta_salida (str): Carpeta donde guardar la gráfica
        split (bool): Si True, divide en dos gráficas
    """
    if split and len(df_municipio) > 19:
        # Primera mitad
        fig, ax = plt.subplots(figsize=(10, 5))
        
        sizes_1 = df_municipio["freq"].iloc[len(df_municipio["freq"])//2:]
        labels_1 = df_municipio["Municipio"].iloc[len(df_municipio["Municipio"])//2:]
        
        bars = ax.barh(labels_1, sizes_1, color=settings.COLORS)
        
        for bar in bars:
            width = bar.get_width()
            if not np.isnan(width):
                ax.text(
                    width + 0.5,
                    bar.get_y() + bar.get_height()/2,
                    f"{int(width)}",
                    va="center"
                )
        
        ax.tick_params(axis="y", labelsize=13)
        plt.tight_layout()
        fig.savefig(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras_1", "pdf"),
            format=settings.PLOT_FORMAT,
            transparent=settings.PLOT_TRANSPARENT
        )
        plt.close()
        
        # Segunda mitad
        fig, ax = plt.subplots(figsize=(10, 5))
        
        sizes_2 = df_municipio["freq"].iloc[:len(df_municipio["freq"])//2]
        labels_2 = df_municipio["Municipio"].iloc[:len(df_municipio["Municipio"])//2]
        
        bars = ax.barh(labels_2, sizes_2, color=settings.COLORS)
        
        for bar in bars:
            width = bar.get_width()
            if not np.isnan(width):
                ax.text(
                    width + 0.5,
                    bar.get_y() + bar.get_height()/2,
                    f"{int(width)}",
                    va="center"
                )
        
        ax.tick_params(axis="y", labelsize=13)
        plt.tight_layout()
        fig.savefig(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras_2", "pdf"),
            format=settings.PLOT_FORMAT,
            transparent=settings.PLOT_TRANSPARENT
        )
        plt.close()
    else:
        # Una sola gráfica
        fig, ax = plt.subplots(figsize=(10, 5))
        
        sizes = df_municipio["freq"]
        labels = df_municipio["Municipio"]
        
        bars = ax.barh(labels, sizes, color=settings.COLORS)
        
        for bar in bars:
            width = bar.get_width()
            if not np.isnan(width):
                ax.text(
                    width + 0.5,
                    bar.get_y() + bar.get_height()/2,
                    f"{int(width)}",
                    va="center"
                )
        
        ax.tick_params(axis="y", labelsize=13)
        plt.tight_layout()
        fig.savefig(
            generador_ruta_guardado(carpeta_salida, "Poblacion_Municipios_Barras", "pdf"),
            format=settings.PLOT_FORMAT,
            transparent=settings.PLOT_TRANSPARENT
        )
        plt.close()
