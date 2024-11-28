from dash import dcc, html
from app.graphs import create_line_chart
from utils.utils import period_to_str

def create_layout(df_region, d):
    # Création du graphique à partir des données
    fig2 = create_line_chart(df_region)

    layout = html.Div([
        # Titre principal
        html.H1(
            children="L'accès à la fibre en France métropolitaine",
            style={'textAlign': 'center', 'color': '#2C3E50', 'fontSize': '40px', 'marginTop': '20px'}
        ),
        
        # Premier graphique avec slider
        dcc.Graph(
            id='graph-with-slider', 
            style={'height': '800px', 'border': '1px solid #D3D3D3', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)', 'margin': '20px auto'}
        ),
        
        # Texte au-dessus du slider
        html.H3(
            children="Choisissez la période",
            style={'textAlign': 'center', 'color': '#34495E', 'fontSize': '24px', 'marginTop': '20px'}
        ),
        
        # Conteneur pour le slider avec style appliqué
        html.Div(
            dcc.Slider(
                step=None,
                value=0,
                marks=d,
                id='periode-slider',
                tooltip={"placement": "bottom", "always_visible": True},
                updatemode='drag',
                included=False
            ),
            style={'width': '80%', 'margin': 'auto', 'padding': '20px 0'}
        ),
        
        # Graphique en ligne
        dcc.Graph(
            id='line-chart', 
            figure=fig2, 
            style={'marginTop': '50px', 'border': '1px solid #D3D3D3', 'borderRadius': '10px', 'boxShadow': '0px 0px 10px rgba(0, 0, 0, 0.1)', 'padding': '10px'}
        ),
        
        # Sous-titre pour la carte
        html.H3(
            children=f"Carte représentant la proportion d'accès à la fibre au {period_to_str()} en France métropolitaine",
            style={'textAlign': 'center', 'color': '#34495E', 'fontSize': '24px', 'marginTop': '50px'}
        ),
        
        # Carte interactive
        html.Iframe(
            id='map', 
            srcDoc=open('data/map/map.html', 'r').read(), 
            width='100%', 
            height='1000', 
            style={'border': 'none', 'marginTop': '20px'}
        )
    ], style={'fontFamily': 'Arial, sans-serif', 'backgroundColor': '#F7F9F9', 'padding': '20px'})
    
    return layout