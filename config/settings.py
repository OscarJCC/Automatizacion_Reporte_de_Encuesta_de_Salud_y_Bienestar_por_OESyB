"""
Configuración centralizada para el sistema de generación de reportes.
Contiene todas las constantes, paletas de colores, listas de búsqueda y mapeos.
"""

import os

# ============================
# RUTAS
# ============================

# Ruta base del proyecto (se configurará en tiempo de ejecución)
RUTA_BASE = None

def set_base_path(path):
    """Configura la ruta base del proyecto."""
    global RUTA_BASE
    RUTA_BASE = path


# ============================
# PALETAS DE COLORES
# ============================

COLORS = [
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
    "#0033CC",  # Azul eléctrico oscuro
    "#E4007C",
    "#5CCE55",
]

COLORS_NIVEL = ['skyblue', 'orange', 'red']


# ============================
# LISTAS DE BÚSQUEDA DE SUSTANCIAS
# ============================

LISTA_BUSQUEDA_DROGA = [
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


# ============================
# MAPEO DE SUSTANCIAS
# ============================

MAPA_SUSTANCIAS = {
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

    'lsd': 'LSD',
    'metanfetamina': 'Metanfetamina',
    'cristal': 'Metanfetamina'
}


# ============================
# CONFIGURACIÓN DE DATOS
# ============================

# Nombres de archivos de datos
DATA_FILE_CSV = "Base de datos - Universidades publicas 2025 Con puntos de corte2 1.csv"
DATA_FILE_EXCEL = "Base de datos - Universidades publicas 2025 (03102025).xlsx"
METADATA_SHEET = "Notas"

# Columnas importantes
COL_UNIVERSIDAD = "Universidad:"
COL_SEXO = "Sexo:"
COL_EDAD = "Edad:"
COL_MUNICIPIO = "Municipio"
COL_ENFERMEDADES = "Indica cuáles de las siguientes enfermedades presentas actualmente o presentaste en el último año:"
COL_CONSUMO_SUSTANCIAS = "CS_3"

# Listas de preguntas para escalas
LIST_PREG_CS = ['CS_1', 'CS_2', 'CS_4', 'CS_4_54', 'CS_4_55', 'CS_5', 'CS_6']
LIST_PREG_RYFF = ['RYFF_1', 'RYFF_2', 'RYFF_3', 'RYFF_4', 'RYFF_5', 'RYFF_6', 'RYFF_7', 'RYFF_8']
LIST_PREG_RS = ['RS_1', 'RS_2', 'RS_3', 'RS_4']

# Géneros
GENEROS = ["Masculino", "Femenino", "Intersexual"]


# ============================
# CONFIGURACIÓN DE CLASIFICACIÓN
# ============================

# Puntos de corte para riesgo de adicción
BINS_ADICCION = [-1, 3, 26, float('inf')]
LABELS_ADICCION = ['Bajo', 'Moderado', 'Alto']

# Puntos de corte para bienestar psicológico (RYFF)
BINS_RYFF = [7, 19, 33, float('inf')]
LABELS_RYFF = ['Bajo', 'Moderado', 'Alto']

# Puntos de corte para riesgo suicida
BINS_SUICIDIO = [-1, 5, float('inf')]
LABELS_SUICIDIO = ['Sin riesgo', 'En riesgo']

# Puntos de corte para ansiedad
BINS_ANSIEDAD = [-1, 7, 10, float('inf')]
LABELS_ANSIEDAD = ['Normal', 'Probable', 'Presente']

# Puntos de corte para depresión
BINS_DEPRESION = [-1, 7, 10, float('inf')]
LABELS_DEPRESION = ['Normal', 'Probable', 'Presente']


# ============================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================

# Tamaños de figura por defecto
FIGSIZE_BARRAS_H = (10, 4)
FIGSIZE_BARRAS_V = (10, 8)
FIGSIZE_CIRCULO = (10, 8)
FIGSIZE_CIRCULO_GRANDE = (15, 9)
FIGSIZE_HORIZONTAL_BAR = (16, 2)

# Configuración de gráficas
PLOT_DPI = 100
PLOT_TRANSPARENT = True
PLOT_FORMAT = "pdf"


# ============================
# CONFIGURACIÓN DE LATEX
# ============================

GEOMETRY_OPTIONS = {
    "margin": "2.5cm"
}

# Información del documento
DOC_TITLE = "Resultados 2025"
DOC_INSTITUTION = "UNIVERSIDAD AUTÓNOMA DE COAHUILA"
DOC_OBSERVATORY = "OBSERVATORIO ESTATAL DE SALUD Y BIENESTAR"
DOC_DATE = "Noviembre 2025"
DOC_FOOTER_LEFT = "VSM"
DOC_HEADER_CENTER = "OESyB"

# Autores
ELABORO = [
    "Dra. Valeria Soto Mendoza - Centro de Investigación en Matemáticas Aplicadas, US",
    "Ing. Oscar Joel Castro Contreras - Centro de Investigación en Matemáticas Aplicadas, US",
    "Ing. Erick Uriel Ruiz Martínez - Centro de Investigación en Matemáticas Aplicadas, US"
]

PRESENTA = [
    "Dra. Bárbara de los Ángeles Pérez Pedraza - Facultad de Psicología, US",
    "Dra. Adriana Méndez Wong",
    "Dr. David Pedroza Escobar - Centro de Investigación Biomédica, UT",
    "Dra. Dealmy Delgadillo Guzmán - Facultad de Medicina, UT",
    "Dra. Diana Berenice Cortes Montelongo",
    "Dra. Edna Idalia Paulina Navarro Oliva",
    "Dra. Griselda de Jesús Granados Udave",
    "Dra Irais Castillo Maldonado - Facultad de Medicina, UT",
    "Dr. José González Tovar - Facultad de Psicología, US",
    "Dr. José Roberto Cantú González",
    "Dr. Juan Bernardo Amezcua Núñez - Facultad de Mercadotecnia, US",
    "Dra. Karla Patricia Valdés García - Facultad de Psicología, US",
    "Dr. Luis Gerardo Vásquez Guajardo",
    "Dra. María del Carmen Flores Ramírez - Escuela de Ciencias de la Comunidad, UT",
    "Dra. Rosa Isabel Garza Sánchez - Facultad de Trabajo Social, US"
]
