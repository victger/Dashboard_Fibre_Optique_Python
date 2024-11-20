import json
import folium
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from utils.utils import *
import pandas as pd
import sys

df_region= nettoyage('Régions')
df_departement= nettoyage('Départements')
df_commune= nettoyage('Communes')

# On modifie les dataframes finales pour exploiter des données dans notre dashboard

df_departement["proportion_de_logements_raccordables"]= df_departement["nombre_de_logements_raccordables"]/df_departement["meilleure_estimation_des_locaux_t2_2022"]
df_departement["classe"]= [str(round_decimals_down(element, 1))+" - "+str(round_decimals_up(element, 1)) for element in df_departement["proportion_de_logements_raccordables"]]
df_departement= df_departement.sort_values(by=['classe'])
tri_an= ['T4 2017', 'T1 2018', 'T2 2018', 'T3 2018', 'T4 2018', 'T1 2019', 'T2 2019', 'T3 2019', 'T4 2019', 'T1 2020', 'T2 2020', 'T3 2020', 'T4 2020', 'T1 2021', 'T2 2021', 'T3 2021', 'T4 2021', 'T1 2022', 'T2 2022']
key= [i for i in range(len(tri_an))]
d= dict(zip(key, tri_an)) # Sert au slider

periode= ["T"+ str(df_region["trimestre"].iloc[index])+" "+str(df_region["annee"].iloc[index]) for index in df_region.index]# On récupère la période avec de l'algorithmique
df_region["periode"]= periode
df_region["proportion_de_logements_raccordables"]= df_region["nombre_de_logements_raccordables"]/df_region["meilleure_estimation_des_locaux_t2_2022"]

df_commune= df_commune[df_commune["trimestre"]==2]
df_commune= df_commune[df_commune["annee"]==2022] # Pour notre carte, on fixe au 2ème trimestre de 2022
df_commune["proportion_de_logements_raccordables_dans_la_commune"]= df_commune["nombre_de_logements_raccordables"]/df_commune["meilleure_estimation_des_locaux_t2_2022"]

# Création de graphes

fig2= px.line(df_region, x="periode", y="proportion_de_logements_raccordables",
                color='nom_region', 
                color_discrete_sequence=px.colors.qualitative.Light24)
fig2.update_layout(title_text= "Évolution de la proportion de logements raccordables dans une région donnée",
                    title_x= 0.5,
                    xaxis_title= "Période",
                    yaxis_title= "Proportion de logements raccordables",
                    legend_title= "Nom de la région")

# Création de la carte

# france_geo= "datagouv-communes.geojson"

# m= folium.Map(location=[46.7555, 2.4252], zoom_start=6)

# folium.Choropleth(
#     geo_data=france_geo,
#     name="choropleth",
#     data=df_commune,
#     columns=["code_commune", "proportion_de_logements_raccordables_dans_la_commune"],
#     key_on='feature.properties.code_commune',
#     fill_color="YlGn",
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name="Proportion",
# ).add_to(m)
# folium.LayerControl().add_to(m)

# m.save('map.html')

# Partie création dashboard

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children= "L'accès à la fibre en France métropolitaine", style= {'textAlign': 'center'}),
    dcc.Graph(id='graph-with-slider', style= {'height': '800px'}),
    html.H3(children="Choisissez la période", style={'textAlign': 'center'}),
    dcc.Slider(
        step= None,
        value=0,
        marks=d,
        id='periode-slider'
    ),
    dcc.Graph(id='line-chart', figure= fig2, style= {'marginTop': '50px'}),
    html.H3(children="Carte répertoriant la proportion d'accès à la fibre au 2ème trimestre de 2022 en France métropolitaine", style={'textAlign': 'center', 'marginTop': '50px'}),
    html.Iframe(id='map', srcDoc=open('map.html', 'r').read(), width= '100%', height= '1000')
    ])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('periode-slider', 'value'),
    )

def update_figure(selected):
    """
    Actualise les données de notre histogramme

    Args :
        selected: période sélectionnée

    """

    filtered_df_departement= df_departement[df_departement["annee"] == int(d.get(selected).split(' ')[1])]
    filtered_df_departement= filtered_df_departement[filtered_df_departement["trimestre"] == int(d.get(selected).split(' ')[0][1])]

    fig = px.bar(filtered_df_departement, x="classe", text="nom_departement")
    fig.update_layout(
            transition_duration=500,
            title_text= "Proportion de logements raccordables en France métropolitaine en fonction du département",
            title_x= 0.5,
            xaxis_title= "Proportion de logements raccordables dans un département",
            yaxis_title= "Nombre de départements correspondant à l'intervalle au "+d.get(selected)
            )
    fig.update_traces(textposition='inside')

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)