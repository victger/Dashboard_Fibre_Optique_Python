from dash import Dash
from utils.utils import process_data, nettoyage
from app.app import launch_app
import sys

# Nettoyage des données
df_region = nettoyage('Régions')
df_departement = nettoyage('Départements')
df_commune = nettoyage('Communes')

# Traitement des données (fonction définie dans utils)
df_departement, df_region, df_commune, d= process_data(df_departement, df_region, df_commune)

# Lancement de l'application avec les DataFrames
launch_app(df_region, df_departement, df_commune, d)