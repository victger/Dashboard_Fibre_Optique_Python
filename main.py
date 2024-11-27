from dash import Dash
from utils.download_file import download_file
from app.app import launch_app

download_file()

from utils.utils import process_data

# Traitement des données (fonction définie dans utils)
df_departement, df_region, df_commune, d= process_data()

# Lancement de l'application avec les DataFrames
launch_app(df_region, df_departement, df_commune, d)