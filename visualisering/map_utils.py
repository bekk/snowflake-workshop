import pandas as pd
import folium
import json

def style_function(feature: dict):
    score = feature["geometry"]["properties"]["score"]
    color = "red"
    if score > 0.33 and score <= 0.66:
        color = "yellow"
    if score > 0.66:
        color = "green"

    return { 'fillColor': color, 'color': "#0000ff40", 'weight': 4, 'fillOpacity': 0.5 }

def generate_map(df: pd.DataFrame) -> folium.Map:
    # Denne funksjonen forventer en Dataframe med kolonnene KOMMUNENAVN, KOMMUNENUMMER, GJENNOMSNITTLIG_KARAKTER, GEOMETRY (Som GeoJSON)
    punkt_for_norge = [62.6252978589571, 10.34580993652344]
    m = folium.Map(location=punkt_for_norge, zoom_start=6)

    for _, row in df.iterrows():
        geo_json_dict = json.loads(row["GEOMETRY"])
        geo_json_dict["properties"] = { "score": row["GJENNOMSNITTLIG_KARAKTER"] }
        geo_json = folium.GeoJson(
            geo_json_dict,
            style_function=style_function,
            tooltip=str(f'{row["KOMMUNENAVN"]}, Score={row["GJENNOMSNITTLIG_KARAKTER"]}')
        )
        geo_json.add_to(m)

    return m
