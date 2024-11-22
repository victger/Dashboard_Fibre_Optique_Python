from dash import Dash
from app.layout import create_layout
from app.callbacks import register_callbacks

def launch_app(df_region, df_departement, df_commune, d):
    # Initialisation de l'application Dash
    app = Dash(__name__)

    # Définition de la mise en page en passant les DataFrames nécessaires
    app.layout = create_layout(df_region, df_commune, d)

    # Enregistrement des callbacks en passant les DataFrames
    register_callbacks(app, df_departement, d)
    
    app.run_server()