import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import unicodedata
import os

from pylatex import (
     Document,
     Figure,
     NoEscape,
     Package,
     Foot,
     Head,
     PageStyle,
)

# ============================
# CODIGO
# ============================

# Funciones ============================

def split_enfermedades(texto):
     # Expresión regular: separa en comas que no estén dentro de paréntesis
     return re.split(r",\s*(?![^(]*\))", texto)

def ajusta_datos_drogas(x):
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

     #Si es NaN -> None
     if texto is None or (isinstance(texto, float) and pd.isna(texto)):
          return None

     #Convertir todo a string para evitar arrays o listas
     texto = str(texto)

     #Buscar sustancia
     for sustancia in lista:
          if sustancia in texto:
               return sustancia

     return None

def generador_ruta_guardado(carpeta, n_archivo, extension=None):
     if extension:
          archivo = f"{n_archivo}.{extension}"
     else:
          archivo = n_archivo
     
     return os.path.join(carpeta, archivo)

#============================ 

# Setup ============================

ruta_base = os.path.dirname(os.path.abspath(__file__))

colors = [
     "#005BBB",  # Azul profundo
     "#6A00FF",  # Morado vibrante
     "#004F67",  # Azul petróleo
     "#B00020",  # Rojo carmín oscuro
     "#007B3E",  # Verde esmeralda oscuro
     "#C74E00",  # Naranja quemado
     "#8A0057",  # Magenta oscuro
     "#002F6C",  # Azul índigo
     "#0B5D1E",  # Verde bosque
     "#7A0026",  # Rojo vino
     "#003F9A",  # Azul real oscuro
     "#00687F",  # Turquesa profundo
     "#4B006E",  # Morado uva
     "#A63A00",  # Naranja óxido
     "#006F5F",  # Verde menta oscuro
     "#5E0038",  # Ciruela oscuro
     "#0033CC",   # Azul eléctrico oscuro
     "#E4007C",
     "#5CCE55",
]

colors_nivel = ['skyblue', 'orange', 'red']

lista_de_busqueda_droga = [
     # tabaco / nicotina
     "tabaco", "cigarro", "cigarros", "fumar", "vape", "vapear",
     "nicotina", "cigarrillo", "cigarrillos",

     # alcohol
     "alcohol", "cerveza", "vino", "licor", "vodka", "tequila", "ron",

     # cannabis
     "marihuana", "mariguana", "cannabis", "mota", "porro", "joint", "blunt",
     "hierba", "weed", "wax", "thc", "hash",

     # estimulantes
     "cafeina", "cafeína", "cafe", "café", "red bull", "monster",
     "cocaína", "cocaina", "perico", "cristal",

     # psicodélicos
     "lsd", "acido", "acido lisergico", "hongos", "psilocibina",

     # otros
     "ketamina", "mdma", "éxtasis", "extasis", "anfetaminas",
     "metanfetamina", "heroina", "heroína", "opio",
]
mapa = {
     'alcohol': 'Alcohol',
     'cerveza': 'Alcohol',
     'ron': 'Alcohol',

     'marihuana': 'Cannabis',
     'mariguana': 'Cannabis',
     'mota': 'Cannabis',
     'cannabis': 'Cannabis',
     'weed': 'Cannabis',
     'thc': 'Cannabis',
     'wax': 'Cannabis',

     'tabaco': 'Tabaco',
     'cigarro': 'Tabaco',
     'cigarrillo': 'Tabaco',
     'nicotina': 'Tabaco',
     'vape': 'Tabaco',
     'fumar': 'Tabaco',

     'cafe': 'Cafeína',
     'cafeina': 'Cafeína',

     #'cocaina': 'cocaína',
     'lsd': 'LSD',
     'metanfetamina': 'Metanfetamina',
     'cristal': 'Metanfetamina'
}

#data_1_d = pd.read_excel(generador_ruta_guardado(ruta_base,"Base de datos - Universidades publicas 2025 (03102025)","xlsx"),sheet_name="Hoja1")
data_1_d = pd.read_csv(generador_ruta_guardado(ruta_base,"Base de datos - Universidades publicas 2025 Con puntos de corte2 1.csv"))

data_2 = pd.read_excel(generador_ruta_guardado(ruta_base,"Base de datos - Universidades publicas 2025 (03102025)","xlsx"),sheet_name="Notas")

data_1_d["Universidad:"] = data_1_d["Universidad:"].replace(
     {"UNIVERSIDAD POLITÉCNICA DE MONCLOVA-10": "UNIVERSIDAD POLITÉCNICA DE MONCLOVA-FRONTERA"}
)

"""
 0.- GENERAL
 1.- UNIVERSIDAD TECNOLÓGICA DE TORREÓN #
 2.- UNIVERSIDAD TECNOLÓGICA DE COAHUILA #
 3.- INSTITUTO TECNOLÓGICO SUPERIOR DE CIUDAD ACUÑA #
 4.- UNIVERSIDAD TECNOLÓGICA DEL NORTE DE COAHUILA #
 5.- UNIVERSIDAD TECNOLÓGICA DE LA REGIÓN CENTRO DE COAHUILA #
 6.- INSTITUTO TECNOLÓGICO DE ESTUDIOS SUPERIORES DE LA REGIÓN # CARBONÍFERA #
 7.- INSTITUTO TECNOLÓGICO SUPERIOR DE MONCLOVA #
 8.- INSTITUTO TECNOLÓGICO SUPERIOR DE SAN PEDRO DE LAS COLONIAS #
 9.- UNIVERSIDAD TECNOLÓGICA DE CIUDAD ACUÑA #
10.- UNIVERSIDAD TECNOLÓGICA DE LA REGIÓN CARBONÍFERA #
11.- UNIVERSIDAD POLITÉCNICA DE MONCLOVA-FRONTERA #
12.- UNIVERSIDAD POLITÉCNICA DE LA REGION LAGUNA #
13.- UNIVERSIDAD POLITÉCNICA DE RAMOS ARIZPE #
14.- UNIVERSIDAD TECNOLÓGICA DE SALTILLO #
15.- UNIVERSIDAD TECNOLÓGICA DE PARRAS DE LA FUENTE #
16.- UNIVERSIDAD POLITÉCNICA DE PIEDRAS NEGRAS #
17.- INSTITUTO TECNOLÓGICO SUPERIOR DE MÚZQUIZ #
"""

universidades = ["GENERAL"]
data_universidades = df_us_universidad = data_1_d["Universidad:"].value_counts().sort_values(ascending=False).reset_index()
universidades += list(data_universidades["Universidad:"])

# Seleccion de universidad
universidad = 0

for universidad in range(len(universidades)):

     t_guardado = "".join([c for c in unicodedata.normalize("NFKD", universidades[universidad]) if not unicodedata.combining(c)]).replace(" ", "_")
     carpeta_salida = os.path.join(ruta_base, f"2025-ReporteCoahuila-{t_guardado}")
     carpeta_N = os.path.join(ruta_base, f"{t_guardado}")
     os.makedirs(carpeta_salida, exist_ok=True)

     if universidad != 0:
          data_1 = data_1_d[data_1_d["Universidad:"] == universidades[universidad]]
     else:
          data_1 = data_1_d.copy()

     # Graficas ============================

     # \subsection{Porcentaje de usuarios por institución}
     df_us_universidad = data_1["Universidad:"].value_counts().sort_values(ascending=True).reset_index()
     df_us_universidad.columns = ["Universidad", "freq"]

     if universidad == 0:
          #------------------------------------------------------
          fig, ax_us_universidad_barras = plt.subplots(figsize=(10,4)) 

          sizes_us_universidad = df_us_universidad["freq"]
          labels_us_universidad = df_us_universidad["Universidad"]

          bars = ax_us_universidad_barras.barh(labels_us_universidad, sizes_us_universidad, color = colors)

          for bar in bars:
               width = bar.get_width()
               ax_us_universidad_barras.text(
                    width * 0.5,                      # dentro de la barra
                    bar.get_y() + bar.get_height()/2,
                    f"{int(width)}",
                    va="center",
                    ha="center",
                    color="white",                    # blanco para contraste
                    fontsize=10
               )

          ax_us_universidad_barras.tick_params(axis="y", labelsize=8)
          
          plt.tight_layout()
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Barras","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------
          fig, ax_us_universidad_circulo = plt.subplots(figsize=(15, 9))

          ax_us_universidad_circulo.set_aspect("equal")

          wedges, _ = ax_us_universidad_circulo.pie(
               sizes_us_universidad,
               labels=None,
               colors=colors,
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

               ax_us_universidad_circulo.text(
                    x, y,
                    f"{sizes_us_universidad.iloc[i]}",
                    ha="center",
                    va="center",
                    fontsize=13,
                    color="white",
                    rotation=rot,
               )

          ax_us_universidad_circulo.legend(
               wedges,
               labels_us_universidad,
               loc="center left",
               bbox_to_anchor=(1.0, 0.5),
               fontsize=15
          )
          
          plt.subplots_adjust(top=0.92, bottom=0.05)
          plt.tight_layout(pad=0)
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Circulo","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------


     # \subsection{Porcentaje de usuarios por sexo}
     df_us_sexo = data_1["Sexo:"].value_counts().sort_values(ascending=False).reset_index()
     df_us_sexo.columns = ["Sexo", "freq"]
     
     #------------------------------------------------------
     fig, ax_us_sexo_barras = plt.subplots(figsize=(10, 8))

     sizes_us_sexo = df_us_sexo["freq"]
     labels_us_sexo = df_us_sexo["Sexo"]

     bars = ax_us_sexo_barras.bar(labels_us_sexo, sizes_us_sexo,color=colors[-3:])

     for bar in bars:
          height = bar.get_height()
          ax_us_sexo_barras.text(
               bar.get_x() + bar.get_width()/2,
               height + 0.5,
               f"{height / sizes_us_sexo.sum() * 100:.2f}%",
               ha="center", va="bottom",
               fontsize=11
          )

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Sexo_Barras","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     fig, ax_us_sexo_circulo = plt.subplots(figsize=(10, 8))

     wedges, _ = ax_us_sexo_circulo.pie(
          sizes_us_sexo,
          labels=None,
          colors=colors[-3:],
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
          
          ax_us_sexo_circulo.text(
               x, y,
               f"{sizes_us_sexo.iloc[i] / sizes_us_sexo.sum() * 100:.2f}%",
               ha="center",
               va="center",
               fontsize=15,
               color="white",
               rotation=rot,
          )
          
     ax_us_sexo_circulo.legend(
          wedges,
          labels_us_sexo,
          title="Sexo",
          loc="center left",
          bbox_to_anchor=(1.05, 0.5),
          fontsize=11
          )

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Sexo_Circulo","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     generos = ["Masculino", "Femenino", "Intersexual"]
          
     df_us_universidad_sexo = data_1[["Universidad:", "Sexo:"]].copy()
     df_us_universidad_sexo.columns = ["Universidad", "Sexo"]
     df_us_universidad_sexo = df_us_universidad_sexo.groupby(["Universidad", "Sexo"]).size().unstack(fill_value=0)
          
     for col in ["Masculino", "Femenino", "Intersexual"]:
          if col not in df_us_universidad_sexo.columns:
               df_us_universidad_sexo[col] = 0
          
     df_us_universidad_sexo = df_us_universidad_sexo[generos]

     if universidad == 0:
          #------------------------------------------------------
          fig, ax_us_universidad_sexo = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

          for ax ,genero, color in zip(ax_us_universidad_sexo, generos, colors[-3:]):

               df_us_sexo = df_us_universidad_sexo[genero].sort_values(ascending=True)
               bars = ax.barh(df_us_sexo.index, df_us_sexo.values, alpha=0.8, color=color)

               for bar in bars:
                    width = bar.get_width()
                    ax.text(width + max(df_us_sexo.values)*0.01,
                         bar.get_y() + bar.get_height()/2,
                         f"{int(width)}",
                         va="center", 
                         fontsize=10)

                    ax.text(0.5, -0.12,
                         f"Total: {df_us_sexo.sum()}",
                         transform=ax.transAxes,
                         ha="center",
                         va="center",
                         fontsize=11,
                         fontweight="bold")

               ax.tick_params(axis="y", labelsize=11)
               ax.set_title(genero) 
               xmax = df_us_universidad_sexo[["Masculino", "Femenino", "Intersexual"]].values.max()
               ax.set_xlim(0, xmax * 1.15)

          plt.tight_layout()
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Sexo","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------

     # \subsection{Porcentaje de usuarios por municipio}
     df_municipio = data_1["Municipio"].value_counts().sort_values(ascending=True)
     df_municipio = df_municipio.reset_index()
     df_municipio.columns = ["Clave", "freq"]

     df_mcm = data_2.iloc[0:38, 6:8]
     df_mcm.columns = ["Municipio","Clave"] 

     df_us_municipio = df_mcm.merge(df_municipio, on="Clave", how="left").sort_values("freq", ascending=True).dropna()

     if len(df_us_municipio) > 19:
          #------------------------------------------------------
          fig, ax_us_municipio_1_barras = plt.subplots(figsize=(10,5)) 

          sizes_us_municipio_1 = df_us_municipio["freq"].iloc[len(df_us_municipio["freq"])//2:]
          labels_us_municipio_1 = df_us_municipio["Municipio"].iloc[len(df_us_municipio["Municipio"])//2:]

          bars = ax_us_municipio_1_barras.barh(labels_us_municipio_1, sizes_us_municipio_1, color = colors)

          for bar in bars:
               width = bar.get_width()
               if pd.isna(width):
                    continue
               ax_us_municipio_1_barras.text(
                    width + 0.5,                     
                    bar.get_y() + bar.get_height()/2, 
                    f"{int(width)}",                  
                    va="center"
               )

          ax_us_municipio_1_barras.tick_params(axis="y", labelsize=13)
          
          plt.tight_layout()
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras_1","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------
          fig, ax_us_municipio_2_barras = plt.subplots(figsize=(10,5)) 

          sizes_us_municipio_2 = df_us_municipio["freq"].iloc[:len(df_us_municipio["freq"])//2]
          labels_us_municipio_2 = df_us_municipio["Municipio"].iloc[:len(df_us_municipio["Municipio"])//2]

          bars = ax_us_municipio_2_barras.barh(labels_us_municipio_2, sizes_us_municipio_2, color = colors)

          for bar in bars:
               width = bar.get_width()
               if pd.isna(width):
                    continue
               ax_us_municipio_2_barras.text(
                    width + 0.5,                     
                    bar.get_y() + bar.get_height()/2, 
                    f"{int(width)}",                  
                    va="center"
               )

          ax_us_municipio_2_barras.tick_params(axis="y", labelsize=13)
          
          plt.tight_layout()
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras_2","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------
     else:
          #------------------------------------------------------
          fig, ax_us_municipio_1_barras = plt.subplots(figsize=(10,5)) 

          sizes_us_municipio_1 = df_us_municipio["freq"]
          labels_us_municipio_1 = df_us_municipio["Municipio"]

          bars = ax_us_municipio_1_barras.barh(labels_us_municipio_1, sizes_us_municipio_1, color = colors)

          for bar in bars:
               width = bar.get_width()
               if pd.isna(width):
                    continue
               ax_us_municipio_1_barras.text(
                    width + 0.5,                     
                    bar.get_y() + bar.get_height()/2, 
                    f"{int(width)}",                  
                    va="center"
               )

          ax_us_municipio_1_barras.tick_params(axis="y", labelsize=13)
          
          plt.tight_layout()
          fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras","pdf"), format="pdf", transparent=True)
          plt.close()
          #------------------------------------------------------

     #\subsection{Porcentaje de usuarios por Enfermedad}
     df_us_enfermedades = data_1["Indica cuáles de las siguientes enfermedades presentas actualmente o presentaste en el último año:"].value_counts().sort_values(ascending=False).reset_index()
     df_us_enfermedades.columns = ["Enfermedad", "Cantidad"]
     df_us_enfermedades = df_us_enfermedades.assign(Enfermedad=df_us_enfermedades["Enfermedad"].apply(split_enfermedades)).explode("Enfermedad")
     df_us_enfermedades = df_us_enfermedades.groupby("Enfermedad", as_index=False)["Cantidad"].sum().sort_values(by="Cantidad", ascending=False)
     df_us_enfermedades["Porcentaje"] = df_us_enfermedades["Cantidad"]/df_us_enfermedades["Cantidad"].sum() * 100
     
     #------------------------------------------------------
     fig, ax_us_enf_barras_1 = plt.subplots(figsize=(18, 5))

     porc_us_enf =df_us_enfermedades["Porcentaje"][1:] 
     sizes_us_enf = df_us_enfermedades["Cantidad"][1:]
     labels_us_enf = df_us_enfermedades["Enfermedad"][1:]

     bars = ax_us_enf_barras_1.barh(labels_us_enf, sizes_us_enf, color = colors)

     for bar in bars:
          width = bar.get_width()
          ax_us_enf_barras_1.text(
               width + 0.5,                     
               bar.get_y() + bar.get_height()/2, 
               f"{int(width)}",                  
               va="center"
          )
          ax_us_enf_barras_1.text(-0.1, 0,
               f"Ninguna: {df_us_enfermedades['Cantidad'].iloc[0]}",
               transform=ax_us_enf_barras_1.transAxes,
               ha="center",
               va="center",
               fontsize=11,
               fontweight="bold")

     ax_us_enf_barras_1.invert_yaxis()
     ax_us_enf_barras_1.tick_params(axis="y", labelsize=13)

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Enfermedades_Barras_1","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     fig, ax_us_enf_barras_2 = plt.subplots(figsize=(18, 5))

     bars = ax_us_enf_barras_2.barh(labels_us_enf, porc_us_enf, color = colors)

     for bar in bars:
          width = bar.get_width()
          ax_us_enf_barras_2.text(
               width + 0.5,                     
               bar.get_y() + bar.get_height()/2, 
               f"{width:.2f}%",
               va="center"
          )
          ax_us_enf_barras_2.text(1.1, 0,
               f"Ninguna: {df_us_enfermedades['Porcentaje'].iloc[0]:.2f}%",
               transform=ax_us_enf_barras_2.transAxes,
               ha="center",
               va="center",
               fontsize=11,
               fontweight="bold")

     ax_us_enf_barras_2.invert_xaxis()
     ax_us_enf_barras_2.yaxis.tick_right()
     ax_us_enf_barras_2.yaxis.set_label_position("right")
     ax_us_enf_barras_2.tick_params(axis="y", labelsize=13)

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Enfermedades_Barras_2","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------

     # \subsection{Porcentaje de usuarios por consumo de sustancias}
     df_drogas = data_1["CS_3"].apply(ajusta_datos_drogas)
     df_drogas = df_drogas[df_drogas != "ninguna"].dropna()
     df_us_drogas = df_drogas.apply(lambda x: contiene_sustancia(x, lista_de_busqueda_droga)).value_counts().reset_index()
     
     df_us_drogas.columns = ['Droga', 'Cantidad']
     df_us_drogas['Droga'] = df_us_drogas['Droga'].apply(lambda x: mapa.get(x, x))
     df_us_drogas = df_us_drogas.groupby('Droga')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=False)
     
     #------------------------------------------------------
     fig, ax_us_drogas = plt.subplots(figsize=(10, 5))

     sizes_us_drogas = df_us_drogas["Cantidad"]
     labels_us_drogas = df_us_drogas["Droga"]

     bars = ax_us_drogas.bar(labels_us_drogas, sizes_us_drogas,color=colors)

     for bar in bars:
          height = bar.get_height()
          ax_us_drogas.text(
               bar.get_x() + bar.get_width()/2,
               height + 0.5,
               f"{height}",
               ha="center", va="bottom",
          )

     ax_us_drogas.tick_params(axis='x', labelrotation=90)

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Consumo_Sustancias","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     # \subsection{Porcentaje de usuarios por Riesgo de adicción}
     list_preg_cs = ['CS_1','CS_2','CS_4','CS_4_54','CS_4_55','CS_5','CS_6']
     df_cs = data_1[list_preg_cs].replace("Opción 4", 0).copy()
     df_cs = df_cs.apply(pd.to_numeric, errors='coerce').fillna(0)
     df_cs_s = df_cs.sum(axis=1)
     df_cs.loc[:,'sum'] = df_cs_s
     df_cs.loc[:,'clasificacion'] = pd.cut(df_cs_s,bins=[-1, 3, 26, float('inf')],labels=['Bajo', 'Moderado', 'Alto'])
     
     conteo_clas_cs = df_cs["clasificacion"].value_counts().sort_index()
     porc_conteo_cs = conteo_clas_cs/conteo_clas_cs.sum()
     
     #------------------------------------------------------
     fig, ax_us_cs = plt.subplots(figsize=(16, 2))
     
     ax_us_cs.set_axis_off()
     
     acum = 0
     
     for (label, valor), color in zip(porc_conteo_cs.items(), colors_nivel):
          ax_us_cs.barh(
               y=0,
               width=valor,
               left=acum,
               color=color
          )
     
          if valor != 0.0:
               ax_us_cs.text(
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
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Riesgo_Adiccion","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     # \subsection{Porcentaje de usuarios por nivel de bienestar psicologico}
     list_preg_ryff = ['RYFF_1','RYFF_2','RYFF_3','RYFF_4','RYFF_5','RYFF_6','RYFF_7','RYFF_8']
     df_ryff = data_1[list_preg_ryff].copy()
     df_ryff_s = df_ryff.sum(axis=1)
     df_ryff.loc[:,'sum'] = df_ryff_s
     df_ryff.loc[:,'clasificacion'] = pd.cut(df_ryff_s,bins=[7, 19, 33, float('inf')],labels=['Bajo', 'Moderado', 'Alto'])
     
     conteo_clas_ryff = df_ryff["clasificacion"].value_counts().sort_index()
     porc_conteo_ryff = conteo_clas_ryff/conteo_clas_ryff.sum()
     
     #------------------------------------------------------
     fig, ax_us_ryff_barras = plt.subplots(figsize=(10, 8))
     
     labels_us_ryff = porc_conteo_ryff.index
     sizes_us_ryff = porc_conteo_ryff.values * 100
     
     bars = ax_us_ryff_barras.bar(labels_us_ryff, sizes_us_ryff,color=colors_nivel[::-1])
     
     for bar in bars:
          height = bar.get_height()
          ax_us_ryff_barras.text(
               bar.get_x() + bar.get_width()/2,
               height + 0.5,
               f"{height:.2f}%",
               ha="center", va="bottom",
               fontsize=11
          )

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Bienestar_Psicologico_Barras","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     fig, ax_us_ryff_circulo = plt.subplots(figsize=(10, 8))
     
     wedges, _ = ax_us_ryff_circulo.pie(
          sizes_us_ryff,
          labels=None,
          colors=colors_nivel[::-1],
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
          
          ax_us_ryff_circulo.text(
               x, y,
               f"{sizes_us_ryff[i]:.2f}%",
               ha="center",
               va="center",
               fontsize=15,
               color="white",
               rotation=rot,
          )
          
     ax_us_ryff_circulo.legend(
          wedges,
          labels_us_ryff,
          #title="ryff",
          loc="center left",
          bbox_to_anchor=(1.05, 0.5),
          fontsize=11
          )

     plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Bienestar_Psicologico_Circulo","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     # \subsection{Porcentaje de usuarios por riesgo de suicidio}
     list_preg_rs = ['RS_1','RS_2','RS_3','RS_4']
     df_rs = data_1[list_preg_rs].copy()
     df_rs_s = df_rs.sum(axis=1)
     df_rs.loc[:,'sum'] = df_rs_s
     df_rs.loc[:,'clasificacion'] = pd.cut(df_rs_s,bins=[-1, 5, float('inf')],labels=['Sin riesgo', 'En riesgo'])
     
     conteo_clas_rs = df_rs["clasificacion"].value_counts().sort_index()
     porc_conteo_rs = conteo_clas_rs/conteo_clas_rs.sum()*100
     
     #------------------------------------------------------
     fig, ax_us_rs = plt.subplots(figsize=(16, 2))
     
     ax_us_rs.set_axis_off()
     
     acum = 0
     
     for (label, valor), color in zip(conteo_clas_rs.items(), colors_nivel[0::3-1]):
          ax_us_rs.barh(
               y=0,
               width=valor,
               left=acum,
               color=color
          )
     
          if valor != 0.0:
               ax_us_rs.text(
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

     #plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Riesgo_Suicidio","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     # \subsection{Porcentaje de usuarios por estado de ansiedad}
     df_ans = data_1["Ansiedad"].copy()
     clasificacion_ans = pd.cut(df_ans,bins=[-1, 7, 10, float('inf')],labels=['Normal', 'Probable', 'Presente'])
     conteo_clas_ans = clasificacion_ans.value_counts().sort_index()
     
     #------------------------------------------------------
     fig, ax_us_ans = plt.subplots(figsize=(16, 2))
     
     ax_us_ans.set_axis_off()
     
     acum = 0
     
     for (label, valor), color in zip(conteo_clas_ans.items(), colors_nivel):
          ax_us_ans.barh(
               y=0,
               width=valor,
               left=acum,
               color=color
          )
     
          if valor != 0.0:
               ax_us_ans.text(
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

     #plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Estado_Ansiedad","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------

     # \subsection{Porcentaje de usuarios por estado de depresión}
     df_depr = data_1["Depresion"].copy()
     clasificacion_depr = pd.cut(df_depr,bins=[-1, 7, 10, float('inf')],labels=['Normal', 'Probable', 'Presente'])
     conteo_clas_depr = clasificacion_depr.value_counts().sort_index()
     
     #------------------------------------------------------
     fig, ax_us_depr = plt.subplots(figsize=(16, 2))
     
     ax_us_depr.set_axis_off()
     
     acum = 0
     
     for (label, valor), color in zip(conteo_clas_depr.items(), colors_nivel):
          ax_us_depr.barh(
               y=0,
               width=valor,
               left=acum,
               color=color
          )
     
          if valor != 0.0:
               ax_us_depr.text(
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

     #plt.tight_layout()
     fig.savefig(generador_ruta_guardado(carpeta_salida,"Poblacion_Estado_Depresion","pdf"), format="pdf", transparent=True)
     plt.close()
     #------------------------------------------------------
     
     # Extracción datos porcentuales ============================

     #! Sexo
     df_us_sexo_porc = data_1["Sexo:"].value_counts().sort_values(ascending=False)
     lista_us_sexo_porc = (df_us_sexo_porc / df_us_sexo_porc.sum() * 100).tolist()

     #! Edad
     edad_media = int(data_1["Edad:"].mean())

     #! Estado Civil
     df_us_estado_civil_porc = data_1["Estado civil"].value_counts().sort_values(ascending=True)
     mayor_us_estado_civil_porc = max((df_us_estado_civil_porc/df_us_estado_civil_porc.sum() * 100).tolist())

     #! Hijos
     df_us_tiene_hijos_porc = data_1["¿Tienes Hijos?"].value_counts().sort_values(ascending=True)
     mayor_us_tiene_hijos_porc = max((df_us_tiene_hijos_porc/df_us_tiene_hijos_porc.sum() * 100).tolist())

     #! Trabajo
     df_us_trabaja_porc = data_1["Trabajas actualmente"].value_counts().sort_values(ascending=True)
     df_us_trabaja_porc = df_us_trabaja_porc/df_us_trabaja_porc.sum() * 100
     us_si_trabaja_porc = 0
     for i in df_us_trabaja_porc.index:
          if i != "No":
               us_si_trabaja_porc += float(df_us_trabaja_porc[i])

     #! Jorndad Laboral
     df_trabajo = data_1["Trabajas actualmente"]
     df_us_jornada = data_1["Tu jornada laboral es de:"]
     df_us_trabaja_si_porc = data_1[df_trabajo != "No"]
     df_us_jornada_porc = df_us_jornada[df_us_trabaja_si_porc.index].value_counts().sort_values(ascending=False)
     us_trabaja_jornada_comp = (df_us_jornada_porc/df_us_jornada_porc.sum() * 100).tolist()[0]

     #! Ingreso Familiar
     df_us_ingreso_familiar = data_1[["Ingreso mensual familiar:"]].value_counts().sort_values(ascending=True)
     df_us_ingreso_familiar = df_us_ingreso_familiar / df_us_ingreso_familiar.sum() * 100
     us_ingreso_familiar_men_20000 = float(df_us_ingreso_familiar.iloc[2:].sum())

     #! Beca
     df_us_beca_proc = data_1["¿Has recibido alguna beca federal, estatal o municipal durante tu trayectoria académica? Especifique el nivel"].value_counts().sort_values(ascending=True)
     df_us_beca_proc = (df_us_beca_proc / df_us_beca_proc.sum() * 100)
     us_beca = 0
     for i in df_us_beca_proc.index:
          if i != "No":
               us_beca += float(df_us_beca_proc[i])

     #! Enfermedades
     mas_enfer_men = df_us_enfermedades.nlargest(6,'Cantidad')['Enfermedad'].tolist()
     mas_enfer_us = df_us_enfermedades.nlargest(6,'Cantidad')['Cantidad'].tolist()
     mas_enfer_us_porc = df_us_enfermedades.nlargest(6,'Cantidad')['Porcentaje'].tolist()

     us_enfermos = 0
     us_enfermos_porc = 0
     for i in range(len(df_us_enfermedades['Enfermedad'])):
          if df_us_enfermedades['Enfermedad'][i] != "Ninguna":
               us_enfermos += int(df_us_enfermedades['Cantidad'][i])
               us_enfermos_porc += float(df_us_enfermedades['Porcentaje'][i])

     #! Horas de sueño
     df_us_horas_sueño = data_1["¿Cuántas horas de sueño tiene al día?"].value_counts().sort_values(ascending=True)
     df_us_horas_sueño = df_us_horas_sueño/df_us_horas_sueño.sum() * 100

     us_sueño_n = df_us_horas_sueño.idxmax()
     us_sueño_max = df_us_horas_sueño[us_sueño_n]

     #! Deporte
     df_us_deporte = data_1["¿Con qué frecuencia practica algún deporte a la semana?"].value_counts().sort_values(ascending=True)
     df_us_deporte = df_us_deporte/df_us_deporte.sum() * 100

     us_deporte = 0
     for i in df_us_deporte.index:
          if i != "No practico":
               us_deporte += df_us_deporte[i]

     #! Salud Mental
     var_salud_mental = "Desordenes psiquiátricos (depresión, ansiedad, trastornos de la personalidad, etc.)"

     us_salud_menta_bad = df_us_enfermedades[df_us_enfermedades["Enfermedad"] == var_salud_mental].iloc[0].tolist()

     #! Drogas
     df_drogas = data_1["CS_3"].apply(ajusta_datos_drogas)
     df_drogas = df_drogas[df_drogas != "ninguna"].dropna()
     df_us_drogas = df_drogas.apply(lambda x: contiene_sustancia(x, lista_de_busqueda_droga)).value_counts()
     df_us_drogas = df_us_drogas.reset_index()
     df_us_drogas.columns = ['Droga', 'Cantidad']
     df_us_drogas['Droga'] = df_us_drogas['Droga'].apply(lambda x: mapa.get(x, x))
     df_us_drogas = df_us_drogas.groupby('Droga')['Cantidad'].sum().reset_index().sort_values('Cantidad', ascending=False)

     us_cons_drogas = df_us_drogas['Cantidad'].sum()
     us_cons_drogas_porc = us_cons_drogas/len(data_1) * 100
     droga_mas_cons_us = df_us_drogas['Droga'].tolist()[0:4]
     droga_mas_cons_us_c = df_us_drogas['Cantidad'].tolist()[0:4]
     partes_droga = [f"{droga} ($n={cant:.0f}$)"for droga, cant in zip(droga_mas_cons_us, droga_mas_cons_us_c)]
     
     #! Nivel de riesgo de adicciones
     us_cs = porc_conteo_cs.values.tolist()
     
     #! Grado de bienestar psicologico
     us_ryff = conteo_clas_ryff.values
     us_ryff_por = sizes_us_ryff.tolist()
     
     #! Riesgo Suicida
     us_rs = conteo_clas_rs.values.tolist()
     us_rs_por = porc_conteo_rs.values.tolist()

     # ============================
     # CONFIGURACIÓN DEL DOCUMENTO
     # ============================

     geometry_options = {
          "margin": "2.5cm"
     }

     doc = Document(geometry_options=geometry_options)

     # Paquetes necesarios
     doc.packages.append(Package("graphicx"))     # Para imágenes
     doc.packages.append(Package("babel", options="spanish"))  # Español opcional
     doc.packages.append(Package("setspace"))     # Para espaciado
     doc.packages.append(Package("titling"))      # Para mover el título
     doc.packages.append(Package("ragged2e"))     # Justify
     doc.packages.append(Package("xcolor"))       # Colores opcionales

     # ============================
     # HEADER AND FOOTER
     # ============================

     header = PageStyle("header")

     # HEADERS
     with header.create(Head("C")):     # CE y CO → solo "C" para PyLaTeX
          header.append("OESyB")
          
     with header.create(Head("R")):
          header.append(NoEscape(r"\rightmark"))

     # FOOTERS
     with header.create(Foot("C")):     # CE y CO → solo "C"
          header.append("Noviembre 2025")

     with header.create(Foot("L")):     # LE y LO → "L"
          header.append("VSM")

     with header.create(Foot("R")):     # RE y RO → "R"
          header.append(NoEscape(r"\thepage"))

     # Attach style
     doc.preamble.append(NoEscape(r"\spanishdecimal{.}"))
     doc.preamble.append(NoEscape(r"\renewcommand{\sectionmark}[1]{\markright{\thesection\ #1}}"))
     header.append(NoEscape(r"\renewcommand{\headrulewidth}{0.4pt}"))
     doc.preamble.append(header)
     doc.change_document_style("header")

     # ============================
     # PORTADA
     # ============================

     #doc.append(NoEscape(r"\begin{titlepage}"))
     doc.append(NoEscape(r"\thispagestyle{empty}"))

     if universidad == 0:
          text_port = f"{universidades[universidad]}ES"
          logo_inst = fr"\vspace{{1.7cm}}"
     else:
          text_port = f"{universidades[universidad]}"
          logo_inst = fr"""\begin{{figure}}[htbp]%
               \centering
               \includegraphics[height=2.5cm]{{Logos/Logo-{text_port}.pdf}}%
          \end{{figure}}"""
          #\begin{{figure}}[htbp]%
          #     \begin{{minipage}}{{0.76\textwidth}}%
          #          \includegraphics[width=\textwidth]{{LogosIM.pdf}}%
          #          \label{{EscudoUAdeC}}%
          #     \end{{minipage}}%
          #     \begin{{minipage}}{{0.32\textwidth}}%
          #          \includegraphics[height=1cm]{{LogoOESyB.pdf}}%
          #          \label{{EscudoOESyB}}%
          #     \end{{minipage}}%
          #\end{{figure}}

     # ----- FILA DE LOGOS -----
     doc.append(NoEscape(fr"""

     \begin{{center}}
          \begin{{figure}}[htbp]%
               \centering
               \includegraphics[width=\textwidth]{{Logos/LogosIM.pdf}}%
          \end{{figure}}
          
          \vspace{{0.7cm}}
          \LARGE
          UNIVERSIDAD AUTÓNOMA DE COAHUILA
          
          \vspace{{0.7cm}}
          \LARGE
          OBSERVATORIO ESTATAL DE SALUD Y BIENESTAR
          
          \vspace{{0.8cm}}	
          \Large
          \textbf{{Resultados 2025}}

          \vspace{{0.3cm}}	
          \Large
          {text_port}
          {logo_inst}
          
          \vspace{{0.8cm}}
          \normalsize	
          ELABORÓ \\
          \vspace{{.3cm}}
          %\large
          \textbf{{Dra. Valeria Soto Mendoza - Centro de Investigación en Matemáticas Aplicadas, US}}\\
          \textbf{{Ing. Oscar Joel Castro Contreras - Centro de Investigación en Matemáticas Aplicadas, US}}\\
          \textbf{{Ing. Erick Uriel Ruiz Martínez - Centro de Investigación en Matemáticas Aplicadas, US}}
          
          \vspace{{0.8cm}}
          \normalsize	
          PRESENTA \\
          \vspace{{.3cm}}
          %\large
          \textbf{{Dra. Bárbara de los Ángeles Pérez Pedraza - Facultad de Psicología, US\\ Dra. Adriana Méndez Wong\\ Dr. David Pedroza Escobar - Centro de Investigación Biomédica, UT\\ Dra. Dealmy Delgadillo Guzmán - Facultad de Medicina, UT\\ Dra. Diana Berenice Cortes Montelongo - \\ Dra. Edna Idalia Paulina Navarro Oliva\\ Dra. Griselda de Jesús Granados Udave\\ Dra Irais Castillo Maldonado - Facultad de Medicina, UT\\ Dr. José González Tovar - Facultad de Psicología, US\\ Dr. José Roberto Cantú González\\ Dr. Juan Bernardo Amezcua Núñez - Facultad de Mercadotecnia, US\\ Dra. Karla Patricia Valdés García - Facultad de Psicología, US\\ Dr. Luis Gerardo Vásquez Guajardo\\ Dra. María del Carmen Flores Ramírez - Escuela de Ciencias de la Comunidad, UT\\ Dra. Rosa Isabel Garza Sánchez - Facultad de Trabajo Social, US}}
          
          %\vspace{{.3cm}}
          %\large
          %\textbf{{OESyB}}\\ Mayo 2023
          
          \vspace{{1.3cm}}
          \today
     \end{{center}}

     \newpage
     \tableofcontents %indice general
     \newpage
     """))

     # ============================
     # INTRODUCCIÓN
     # ============================

     if universidad == 0:
          text_ref = f"correspondientes al nivel {universidades[universidad]}"
     else:
          text_ref = f"correspondientes a {universidades[universidad]}"

     doc.append(NoEscape(rf"""
     \section{{INTRODUCCIÓN}}\label{{sec:int}}

          La salud mental y el bienestar de los estudiantes universitarios han cobrado una relevancia creciente en el ámbito académico y de salud pública, debido a la identificación de múltiples factores que pueden afectar su desempeño y calidad de vida. La Encuesta de Salud y Bienestar aplicada a los estudiantes de educación superior en 2025 reveló una alta prevalencia de trastornos como ansiedad y depresión, así como un considerable consumo de alcohol y tabaco en los universitarios de las unidades Saltillo, Torreón y Norte. Estos hallazgos subrayan la necesidad de evaluar de manera continua la salud de la comunidad estudiantil, a fin de generar estrategias preventivas y promover intervenciones oportunas.

          Los primeros años universitarios son una etapa de importantes transiciones y desafíos, en la que los estudiantes deben adaptarse a nuevas exigencias académicas, sociales y económicas. Estas condiciones pueden incrementar el riesgo de desarrollar problemas de salud mental, particularmente en jóvenes que enfrentan condiciones socioeconómicas adversas o que carecen de redes de apoyo. De acuerdo con estudios recientes, la presencia de factores como el estrés financiero, la inseguridad alimentaria y la falta de acceso a servicios de salud pueden exacerbar síntomas de ansiedad y depresión en poblaciones universitarias (González et al., 2023).

          Asimismo, la Organización Mundial de la Salud (OMS, 2023) ha advertido que el consumo de sustancias como alcohol y tabaco sigue siendo un problema latente en este grupo etario, asociado a intentos de regulación emocional y a contextos de socialización poco saludables.

          En este contexto, la Encuesta de Salud y Bienestar del OESyB tiene
          como objetivo actualizar y ampliar el conocimiento sobre el estado de salud de los estudiantes de nuevo ingreso, evaluando no solo aspectos psicológicos como la ansiedad, la depresión y el riesgo suicida, sino también variables económicas, la presencia de enfermedades crónicas y el consumo de sustancias. La inclusión de estos factores permitirá un análisis integral del bienestar estudiantil, favoreciendo la identificación de grupos vulnerables y la implementación de estrategias institucionales más eficaces para el cuidado de su salud.
          
          Finalmente, es importante señalar que el presente resumen se elaboró a partir de los datos {text_ref} de la encuesta, con el fin de ofrecer una visión amplia del estado de salud y bienestar de la población estudiantil evaluada.
     """))

     # ============================
     # RESUMEN EJECUTIVO
     # ============================

     caracteristicas_socioeconomicas = fr"""
          El análisis de la población estudiantil muestra que los hombres, representando el ${lista_us_sexo_porc[0]:.2f}\%$, mientras que las mujeres constituyen el ${lista_us_sexo_porc[1]:.2f}\%$ y el ${lista_us_sexo_porc[2] if len(lista_us_sexo_porc) > 2 else 0.0:.2f}\%$ se identifica como intersexual. La edad promedio de los estudiantes es de ${edad_media}$ años.
          
          En términos de estado civil, se observa que la gran mayoría de los estudiantes son solteros (${mayor_us_estado_civil_porc:.2f}\%$) y no tienen hijos (${mayor_us_tiene_hijos_porc:.2f}\%$), lo que refleja que se trata, en su mayoría, de una población joven y en etapa de formación académica.

          Respecto a la situación laboral, el ${us_si_trabaja_porc:.2f}\%$ de los estudiantes se encuentra trabajando. De este grupo, más de la mitad (${us_trabaja_jornada_comp:.2f}\%$) realiza una jornada laboral de tiempo completo, mientras que el resto cumple con jornadas parciales o flexibles.
          
          En lo referente al ingreso familiar, la mayoría de los estudiantes (${us_ingreso_familiar_men_20000:.2f}\%$) proviene de hogares cuyos ingresos mensuales son iguales o inferiores a \$20000 pesos, lo que indica que gran parte de la población estudiantil pertenece a familias con ingresos medios y bajos.
          
          Finalmente, se destaca que el ${us_beca:.2f}\%$ de los estudiantes ha recibido algún tipo de beca durante su formación académica, lo que evidencia la importancia de los apoyos económicos para facilitar la continuidad educativa y el acceso a oportunidades de estudio.
     """

     caracterisitcas_salud_fisica = fr"""
          Del total de estudiantes encuestados, ${us_enfermos:.0f}$ reportaron tener alguna enfermedad crónica, lo que representa el ${us_enfermos_porc:.2f}\%$ de la población estudiantil. En cuanto a la prevalencia de enfermedades específicas, la más mencionada fue {mas_enfer_men[1]} ($n = {mas_enfer_us[1]:.0f}$), seguida por {mas_enfer_men[4]} ($n = {mas_enfer_us[4]:.0f}$). Esta información permite identificar las condiciones de salud más frecuentes entre los estudiantes y orientar acciones preventivas y de atención médica.
          
          Respecto a los hábitos de sueño, casi la mitad de los estudiantes (${us_sueño_max:.2f}\%$) reporta dormir entre {us_sueño_n} al día, lo que se encuentra dentro de los rangos recomendados para mantener un adecuado bienestar físico y cognitivo.
          
          Finalmente, en lo relativo a la actividad física, ${us_deporte:.2f}\%$ de los estudiantes practica algún deporte al menos 1-2 veces por semana, lo que refleja un nivel moderado de actividad física dentro de la población estudiantil.
     """
     
     riesgo_adiccion = (
     "no se registraron casos en la categoría de riesgo alto, lo que sugiere que no se identificaron individuos con un nivel crítico de riesgo."
     if us_cs[2] == 0
     else f"se registró un ${us_cs[2]:.2f}\\%$ de casos en la categoría de riesgo alto, lo que sugiere que existe un grupo que requiere especial atención."
     )

     caracteristicas_salud_mental = rf"""
     En relación con la salud mental, se identificó que un total de {us_salud_menta_bad[1]:.0f} estudiantes reportaron presentar {us_salud_menta_bad[0]}, lo que corresponde al {us_salud_menta_bad[2]:.2f}\% de toda la población estudiantil encuestada.

     En cuanto al consumo de sustancias, el {us_cons_drogas_porc:.2f}\% de estudiantes (n = {us_cons_drogas}) indicó consumir alguna droga. Dentro de este grupo, las sustancias más reportadas fueron {", ".join(partes_droga[:-1]) + " y " + partes_droga[-1] if len(partes_droga) > 1 else partes_droga[0]}.

     Respecto al nivel de riesgo de adicción: {riesgo_adiccion}

     En cuanto al bienestar psicológico, los resultados muestran que {us_ryff[0]} estudiantes ({us_ryff_por[0]:.2f}\%) se encuentran en el nivel bajo. Por otro lado, {us_ryff[1]} estudiantes ({us_ryff_por[1]:.2f}\%) se sitúan en un nivel moderado de bienestar. Finalmente, {us_ryff[2]} estudiantes ({us_ryff_por[2]:.2f}\%) muestran un nivel alto de bienestar psicológico.

     En cuanto al riesgo suicida, se encontró que 
     \begin{{center}}
          {{\color{{red}}\fontsize{{20}}{{36}}\selectfont \textbf{{{us_rs[1]} estudiantes ({us_rs_por[1]:.2f}\%)}}}}
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

     # ============================
     # POBLACIÓN
     # ============================

     doc.append(NoEscape(fr"""
     \section{{RESULTADOS}}\label{{sec:pob}}

     En cuanto a la composición de la muestra, los datos incluyen información proporcionada por {len(data_1)} estudiantes {text_ref}, lo que permite analizar las condiciones de salud, el bienestar y los factores asociados, garantizando que los resultados reflejen las características del grupo evaluado.

     """))

     if universidad == 0:
          with doc.create(Figure(position="htbp")) as plot:
               plot.append(NoEscape(r"""
                    \subsection{Porcentaje de usuarios por institución}
                    \vspace{-0.5em}
               """))
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Barras","pdf"), width=NoEscape(r"\linewidth"))
               plot.append(NoEscape(r"\vspace{-0.5em}"))
               #plot.append(NoEscape(r"\par"))

          with doc.create(Figure(position="htbp")) as plot:
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Circulo","pdf"), width=NoEscape(r"\linewidth"))
               plot.append(NoEscape(r"\vspace{-0.5em}"))

     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por sexo}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Sexo_Barras","pdf"), width=NoEscape(r"0.5\linewidth"))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Sexo_Circulo","pdf"), width=NoEscape(r"0.5\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          plot.append(NoEscape(r"\par"))
          if universidad == 0:
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Universidades_Sexo","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          #plot.add_caption("Figura en formato vectorial (PDF).")

     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por municipio}
               \vspace{-0.5em}
          """))
          if len(df_us_municipio) > 19:
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras_1","pdf"), width=NoEscape(r"0.5\linewidth"))
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras_2","pdf"), width=NoEscape(r"0.5\linewidth"))
          else:
               plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Municipios_Barras","pdf"), width=NoEscape(r"0.5\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))

     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por enfermedad}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Enfermedades_Barras_1","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          plot.append(NoEscape(r"\par"))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Enfermedades_Barras_2","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          #plot.add_caption("Figura en formato vectorial (PDF).")
          
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por consumo de sustancias}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Consumo_Sustancias","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por nivel de riesgo de adicción}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Riesgo_Adiccion","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
     
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por grado de bienestar psicológico}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Bienestar_Psicologico_Circulo","pdf"), width=NoEscape(r"0.5\linewidth"))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Bienestar_Psicologico_Barras","pdf"), width=NoEscape(r"0.5\linewidth"))
          
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por riesgo de suicidio}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Riesgo_Suicidio","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por estado de ansiedad}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Estado_Ansiedad","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
          
     with doc.create(Figure(position="htbp")) as plot:
          plot.append(NoEscape(r"""
               \subsection{Porcentaje de usuarios por estado de depresión}
               \vspace{-0.5em}
          """))
          plot.add_image(generador_ruta_guardado(carpeta_salida,"Poblacion_Estado_Depresion","pdf"), width=NoEscape(r"\linewidth"))
          plot.append(NoEscape(r"\vspace{-0.5em}"))
     # ============================
     # GENERAR PDF
     # ============================

     doc.generate_pdf(
          generador_ruta_guardado(ruta_base,fr"2025-ReporteCoahuila-{t_guardado}"),
          clean_tex=False
     )