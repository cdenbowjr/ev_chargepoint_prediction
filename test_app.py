# import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
# import flask
from flask import Flask
import json
# from pandas.io.json import json_normalize
import numpy as np
from shapely.geometry import Point,Polygon,LineString,MultiPolygon
import folium
# import plotly.graph_objs as go

# Regular expressions and textual editing
# import re

from app import functions_for_project as ffp
# from src.data import preprocessing_functions as ppf
from data.raw import data_dictionary as data_d


# from sklearn.preprocessing import StandardScaler

msoa_uk = ffp.load_geojson('data/raw/geo_spatial/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_simple.geojson')

df = pd.read_csv('data/processed/full_processed_data.csv')
central_london = ['City of London','Camden','Greenwich','Hackney','Hammersmith and Fulham','Islington','Kensington and Chelsea','Lambeth','Lewisham','Southwark','Tower Hamlets','Wandsworth','Westminster']

# scaler = StandardScaler()
# chrg_select = pd.DataFrame(ppf.ColumnSelector('charge_points').fit_transform(df).values.reshape(-1,1))
# df['charge_points'] = ppf.FeatureLogTransform().fit_transform(chrg_select)


df = pd.merge(df, msoa_uk, left_on='msoa11cd', right_on='properties.msoa11cd')

lad = [{'label':area, 'value':area} for area in df.lad13nm.unique()]

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
#
#
def plot_area(merged_df, feature_var, *args):

    
    try:
        search_area = merged_df[merged_df['properties.msoa11nm'].str.contains('|'.join(args))]
        search_area_json = ffp.df_to_geojson(search_area,
                                         ['properties.msoa11cd', 'properties.msoa11nm', 'properties.objectid',
                                          'properties.st_areashape', 'properties.st_lengthshape'])

        with open('data/processed/search.geojson', 'w') as json_file:
            json.dump(search_area_json, json_file)

        start_lat = search_area.apply(centroid_calc, axis=1).apply(lambda x: x[0]).mean()
        start_lon = search_area.apply(centroid_calc, axis=1).apply(lambda x: x[1]).mean()

        area_map = folium.Map(location=(start_lat, start_lon), zoom_start=11)

        area_map.choropleth(geo_data='data/processed/search.geojson', data=search_area,
                            columns=["properties.msoa11cd", feature_var],
                            key_on='feature.properties.msoa11cd', fill_color='Spectral_r', highlight=True, name="areas",
                            legend_name=data_d.EV_britain().description[feature_var])

        folium.LayerControl().add_to(area_map)
        area_map.save("data/processed/search.html")

    except:
        print("This is not a council area in London")
        print(zip(search_area['properties.msoa11nm'],
                  search_area[['geometry.type', 'geometry.coordinates']].apply(centroid_calc, axis=1)))

#print(data_d.EV_britain().description["income_score"])
# print(plot_area(merged_df,"crime_score","Southwark"))


server = Flask(__name__)
app = dash.Dash('__name__')

app.layout = html.Div(
    [html.Div(
        [html.H1('Correlations'),
         dcc.Graph(id='graph'),
         html.H3('Feature'),
         dcc.Dropdown(id='var1',value='income_score',options=[{'label':x,'value':x} for x in df.columns[4:]]),
         html.Div(id='text1',children='...waiting'),
         html.H3('Target Variable'),
         dcc.Dropdown(id='var2',value='charge_points',options=[{'label':x,'value':x} for x in df.columns[4:]]),
         html.Div(id='text2',children='...waiting')
         ],style= {'width': '50%', 'display': 'inline-block'})
    ]
)

@app.callback(Output('text1','children'),[Input('var1','value')])
def definitions(value):
    return data_d.EV_britain().description[value]

@app.callback(Output('text2','children'),[Input('var2','value')])
def definitions(value):
    return data_d.EV_britain().description[value]

@app.callback(Output('map','srcDoc'),[Input('local_a','value'),Input('var2','value')])

def remap(area,target):
    plot_area(df, target, *area)
    print(*area,target)
    return open('data/processed/search.html','r').read()

@app.callback(Output('graph', 'figure'),
               [Input('var1', 'value'),Input('var2', 'value')])

def clean_data(value1,value2):
    #print(df[value2])
    return {
                                     'data': [
                                         dict(
                                             x=df[value1],
                                             y=df[value2],
                                             #text=merged_df[merged_df['lad13nm'] == i]['metropolitan'],
                                             mode='markers',
                                             opacity=0.7,
                                             marker={
                                                 'color':'red',
                                                 'size': 4,
                                                 'line': {'width': 0.5, 'color': 'black'}
                                             },

                                         )
                                     ],
                                     'layout': dict(
                                         xaxis={'type': 'linear', 'title': value1},
                                         yaxis={'type': 'linear','title': value2},
                                         margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                                         legend={'x': 0, 'y': 1},
                                         hovermode='closest'
                                     )
                                 }
#
# app.layout = html.Div([html.H1(id='title',children='Hello'),
#     html.Iframe(id='choropleth',srcDoc=open('data/processed/search.html','r').read(),width='100%',height='600'),
#     html.Label('Dropdown'),
#     dcc.Dropdown(id='my-drop',options=lad,value='Southwark'),
#
#     html.Div(id='intermediate-value')
#
#
# ],style= {'width': '100%', 'display': 'inline-block'})


if __name__ == "__main__":
    #webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)