import folium

def create_map():
    # Création de la carte choroplèthe
    france_geo = "data/datagouv-communes.geojson"
    df_commune = pd.read_csv("data/Communes.csv")  # Remplacer par le bon chemin de fichier
    m = folium.Map(location=[46.7555, 2.4252], zoom_start=6)

    folium.Choropleth(
        geo_data=france_geo,
        name="choropleth",
        data=df_commune,
        columns=["code_commune", "proportion_de_logements_raccordables_dans_la_commune"],
        key_on='feature.properties.code_commune',
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Proportion"
    ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save('data/map.html')