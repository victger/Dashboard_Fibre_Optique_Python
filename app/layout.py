from dash import dcc, html
from app.graphs import create_line_chart
from utils.utils import period_to_str

def create_layout(df_region,d):
    # Création du graphique à partir des données
    fig2 = create_line_chart(df_region)
    
    layout = html.Div([
        html.H1(children="L'accès à la fibre en France métropolitaine", style={'textAlign': 'center'}),
        dcc.Graph(id='graph-with-slider', style={'height': '800px'}),
        html.H3(children="Choisissez la période", style={'textAlign': 'center'}),
        dcc.Slider(
            step=None,
            value=0,
            marks=d,
            id='periode-slider'
        ),
        dcc.Graph(id='line-chart', figure=fig2, style={'marginTop': '50px'}),
        html.H3(children=f"Carte représentant la proportion d'accès à la fibre au {period_to_str()} en France métropolitaine", style={'textAlign': 'center', 'marginTop': '50px'}),
        html.Iframe(id='map', srcDoc=open('data/map/map.html', 'r').read(), width='100%', height='1000')
    ])
    return layout