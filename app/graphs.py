import plotly.express as px

# Fonction pour créer le graphique linéaire
def create_line_chart(df_region):
    fig2 = px.line(
        df_region, 
        x="periode", 
        y="proportion_de_logements_raccordables",
        color='nom_region', 
        color_discrete_sequence=px.colors.qualitative.Light24
    )
    fig2.update_layout(
        title_text="Évolution de la proportion de logements raccordables dans une région donnée",
        title_x=0.5,
        xaxis_title="Période",
        yaxis_title="Proportion de logements raccordables",
        legend_title="Nom de la région"
    )
    return fig2