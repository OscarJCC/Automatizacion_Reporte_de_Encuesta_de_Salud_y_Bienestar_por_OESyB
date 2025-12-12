"""
Módulo de visualizaciones de salud mental.
Contiene funciones para generar gráficas de riesgo de adicción, bienestar psicológico,
riesgo de suicidio, ansiedad y depresión.
"""

import matplotlib.pyplot as plt
from config import settings
from src.utils.file_utils import generador_ruta_guardado


def plot_addiction_risk(porc_conteo_cs, carpeta_salida):
    """
    Genera gráfica horizontal de riesgo de adicción.
    
    Args:
        porc_conteo_cs (pd.Series): Series con porcentajes por nivel de riesgo
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_HORIZONTAL_BAR)
    
    ax.set_axis_off()
    
    acum = 0
    
    for (label, valor), color in zip(porc_conteo_cs.items(), settings.COLORS_NIVEL):
        ax.barh(
            y=0,
            width=valor,
            left=acum,
            color=color
        )
        
        if valor != 0.0:
            ax.text(
                acum + valor/2,
                0,
                f"{valor*100:.2f}%\nRiesgo\n{label}",
                ha='center',
                va='center',
                fontsize=14,
                color='black'
            )
        
        acum += valor
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Riesgo_Adiccion", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_psychological_wellbeing_bar(labels_ryff, sizes_ryff, carpeta_salida):
    """
    Genera gráfica de barras de bienestar psicológico.
    
    Args:
        labels_ryff: Etiquetas de niveles
        sizes_ryff: Porcentajes
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_BARRAS_V)
    
    bars = ax.bar(labels_ryff, sizes_ryff, color=settings.COLORS_NIVEL[::-1])
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width()/2,
            height + 0.5,
            f"{height:.2f}%",
            ha="center", va="bottom",
            fontsize=11
        )
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Bienestar_Psicologico_Barras", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_psychological_wellbeing_pie(labels_ryff, sizes_ryff, carpeta_salida):
    """
    Genera gráfica de pastel de bienestar psicológico.
    
    Args:
        labels_ryff: Etiquetas de niveles
        sizes_ryff: Porcentajes
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    import numpy as np
    
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_CIRCULO)
    
    wedges, _ = ax.pie(
        sizes_ryff,
        labels=None,
        colors=settings.COLORS_NIVEL[::-1],
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
            f"{sizes_ryff[i]:.2f}%",
            ha="center",
            va="center",
            fontsize=15,
            color="white",
            rotation=rot,
        )
    
    ax.legend(
        wedges,
        labels_ryff,
        loc="center left",
        bbox_to_anchor=(1.05, 0.5),
        fontsize=11
    )
    
    plt.tight_layout()
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Bienestar_Psicologico_Circulo", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_suicide_risk(conteo_clas_rs, carpeta_salida):
    """
    Genera gráfica horizontal de riesgo de suicidio.
    
    Args:
        conteo_clas_rs (pd.Series): Series con conteo por nivel de riesgo
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_HORIZONTAL_BAR)
    
    ax.set_axis_off()
    
    acum = 0
    
    for (label, valor), color in zip(conteo_clas_rs.items(), settings.COLORS_NIVEL[0::2]):
        ax.barh(
            y=0,
            width=valor,
            left=acum,
            color=color
        )
        
        if valor != 0.0:
            ax.text(
                acum + valor/2,
                0,
                f"{valor/conteo_clas_rs.sum()*100:.2f}%\n(n = {valor})\n{label}",
                ha='center',
                va='center',
                fontsize=14,
                color='black'
            )
        
        acum += valor
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Riesgo_Suicidio", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_anxiety(conteo_clas_ans, carpeta_salida):
    """
    Genera gráfica horizontal de estado de ansiedad.
    
    Args:
        conteo_clas_ans (pd.Series): Series con conteo por nivel de ansiedad
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_HORIZONTAL_BAR)
    
    ax.set_axis_off()
    
    acum = 0
    
    for (label, valor), color in zip(conteo_clas_ans.items(), settings.COLORS_NIVEL):
        ax.barh(
            y=0,
            width=valor,
            left=acum,
            color=color
        )
        
        if valor != 0.0:
            ax.text(
                acum + valor/2,
                0,
                f"{valor/conteo_clas_ans.sum()*100:.2f}%\n(n = {valor})\n{label}",
                ha='center',
                va='center',
                fontsize=14,
                color='black'
            )
        
        acum += valor
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Estado_Ansiedad", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()


def plot_depression(conteo_clas_depr, carpeta_salida):
    """
    Genera gráfica horizontal de estado de depresión.
    
    Args:
        conteo_clas_depr (pd.Series): Series con conteo por nivel de depresión
        carpeta_salida (str): Carpeta donde guardar la gráfica
    """
    fig, ax = plt.subplots(figsize=settings.FIGSIZE_HORIZONTAL_BAR)
    
    ax.set_axis_off()
    
    acum = 0
    
    for (label, valor), color in zip(conteo_clas_depr.items(), settings.COLORS_NIVEL):
        ax.barh(
            y=0,
            width=valor,
            left=acum,
            color=color
        )
        
        if valor != 0.0:
            ax.text(
                acum + valor/2,
                0,
                f"{valor/conteo_clas_depr.sum()*100:.2f}%\n(n = {valor})\n{label}",
                ha='center',
                va='center',
                fontsize=14,
                color='black'
            )
        
        acum += valor
    
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(
        generador_ruta_guardado(carpeta_salida, "Poblacion_Estado_Depresion", "pdf"),
        format=settings.PLOT_FORMAT,
        transparent=settings.PLOT_TRANSPARENT
    )
    plt.close()
