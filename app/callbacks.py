from dash import Input, Output
import plotly.express as px

def register_callbacks(app, df_departement, d):
    @app.callback(
        Output('graph-with-slider', 'figure'),
        Input('periode-slider', 'value'),
    )
    def update_figure(selected):
        """
        Actualise les données de l'histogramme en fonction de la période sélectionnée
        """
        # Utilisation du dictionnaire `d` passé comme paramètre
        periode = d.get(selected)
        annee = int(periode.split(' ')[1])
        trimestre = int(periode.split(' ')[0][1])

        # Filtrer les données en fonction de l'année et du trimestre sélectionnés
        filtered_df_departement = df_departement[(df_departement["annee"] == annee) &
                                                 (df_departement["trimestre"] == trimestre)]

        # Créer le graphique avec Plotly
        fig = px.bar(filtered_df_departement, x="classe", text="nom_departement")
        fig.update_layout(
            transition_duration=500,
            title_text=f"Proportion de logements raccordables en France métropolitaine en fonction du département au {periode}",
            title_x=0.5,
            xaxis_title="Proportion de logements raccordables dans un département",
            yaxis_title=f"Nombre de départements correspondant à l'intervalle au {periode}"
        )
        fig.update_traces(textposition='inside')

        return fig