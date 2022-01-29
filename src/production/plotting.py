import json
import pandas as pd
import requests
import re
import folium
from folium import Map, Marker, LayerControl, Choropleth
from shapely.geometry import Polygon
from src.data.data_dictionary import ev_britain


def load_geojson(filepath):
    try:
        with open(filepath) as file:
            data = json.load(file)

        return pd.json_normalize(data=data['features'])

    except FileNotFoundError:
        data = requests.get(filepath).json()
        return pd.json_normalize(data=data['features'])


# Defining function to convert dataframe back to geojson
def df_to_geojson(df, properties):
    geojson = {'type': 'FeatureCollection', 'features': []}
    for _, row in df.iterrows():
        if row['geometry.type'] == "Polygon":
            feature = {'type': 'Feature',
                       'properties': {},
                       'geometry': {'type': 'Polygon', 'coordinates': []}}
        else:
            feature = {'type': 'Feature',
                       'properties': {},
                       'geometry': {'type': 'MultiPolygon', 'coordinates': []}}
        feature['geometry']['coordinates'] = row["geometry.coordinates"]

        for prop in properties:
            feature['properties'][re.search(r"properties.(\w.*)", prop).group(1)] = row[prop]
        geojson['features'].append(feature)
    return geojson


# Function to extract centroids from polygons and multipolygons
def centroid_calc(x):
    if x['geometry.type'] == "Polygon":
        lat = Polygon(x['geometry.coordinates'][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0]).centroid.xy[0][0]
        return lat, long
    else:

        lat = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[1][0]
        long = Polygon(x['geometry.coordinates'][0][0]).centroid.xy[0][0]

        return lat, long


def plot_area(merged_df, feature_var, lat=1, long=1, *args):
    try:
        search_area = merged_df[merged_df['properties.msoa11nm'].str.contains(
            '|'.join(args))]
        search_area_json = df_to_geojson(search_area, [
            'properties.msoa11cd', 'properties.msoa11nm',
            'properties.objectid', 'properties.st_areashape',
            'properties.st_lengthshape'
        ])

        with open('search.geojson', 'w') as json_file:
            json.dump(search_area_json, json_file)

        start_lat = search_area.apply(centroid_calc,
                                      axis=1).apply(lambda x: x[0]).mean()
        start_lon = search_area.apply(centroid_calc,
                                      axis=1).apply(lambda x: x[1]).mean()

        area_map = Map(location=(start_lat, start_lon), zoom_start=11)
        legend_name = ev_britain.description[feature_var]

        Choropleth(
            geo_data='search.geojson',
            data=search_area,
            columns=["properties.msoa11cd", feature_var],
            key_on='feature.properties.msoa11cd',
            fill_color='Spectral_r',
            highlight=True,
            name="areas",
            legend_name=legend_name).add_to(area_map)

        Marker(location=(lat, long)).add_to(area_map)

        LayerControl().add_to(area_map)
        area_map.save("search.html")

    except KeyError:

        print("This is not a council area in London")
