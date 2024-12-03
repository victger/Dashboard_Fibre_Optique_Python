from dash import Dash
from app.layout import create_layout
from app.map import create_map
from app.callbacks import register_callbacks

def launch_app(df_region, df_departement, df_commune, d):

    # Initialisation de l'application Dash
    app = Dash(__name__)

    create_map(df_commune)

    # Définition de la mise en page en passant les DataFrames nécessaires
    app.layout = create_layout(df_region, d)

    # Enregistrement des callbacks en passant les DataFrames
    register_callbacks(app, df_departement, d)
    
    app.run_server(host="0.0.0.0", port=8050)