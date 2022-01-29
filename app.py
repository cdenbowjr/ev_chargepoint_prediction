#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import joblib
import requests

import dash
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

from src.data.data_dictionary import ev_britain
from src.production.plotting import load_geojson, plot_area
from src.production.navigation_bar import navbar_style, navbar
from src.production.layout import correlation_graph, geographic_map

# GET DATA BLOCK
df = pd.read_csv(
    'http://www.data4apurpose.com/client_html/full_processed_data.csv')

# GET GEODATA BLOCK
msoa_uk = load_geojson(
    'http://www.data4apurpose.com/client_html'
    '/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_ultra_simple.geojson'
)

# GET DATA DICTIONARY
data_diction = ev_britain.description
central_london = ev_britain.central_london
greater_london = ev_britain.greater_london

# GET RANDOM LOCATION
random_url = "http://api.postcodes.io/random/postcodes"
random_request = requests.get(random_url).json()['result']
random_postcode, random_district = random_request['postcode'], random_request['admin_district']

# GET PREDICTIVE MODEL
logr_model = joblib.load('./models/logistic_regression_model')

# PERFORM DATA TRANSFORMATIONS
lad = [{'label': area, 'value': area} for area in df.lad13nm.unique()]
df = pd.merge(df, msoa_uk, left_on='msoa11cd', right_on='properties.msoa11cd')

app = dash.Dash('__name__', external_stylesheets=navbar_style)
server = app.server

# CREATE APP LAYOUT
app.layout = html.Div([
    navbar,
    correlation_graph(df),
    geographic_map(random_postcode, random_district, lad)
])


# CREATE APP INTERACTIVITY

@app.callback([
    Output('result', 'children'),
    Output('msoa_loc', 'children'),
    Output('lad_loc', 'children'),
    Output('prob', 'children'),
    Output('postcode', 'disabled')
], [Input('postcode', 'value'),
    Input('submit-button', 'n_clicks')])
def find_pcd(value, clicks):
    the_text = "No result"
    msoa_description = "No MSOA"
    lad_description = "No Local Authority"
    prediction_prob = "No probability"
    disabled = False
    url = "https://api.postcodes.io/postcodes/" + value
    f = requests.get(url).json()
    msoa_nm = f['result']['msoa']
    if clicks > 0:
        msoa_description = f"MSOA: {df[df.msoa11nm == msoa_nm]['msoa11nm'].values[0]}"
        lad_description = f"Local Authority of {df[df.msoa11nm == msoa_nm]['lad13nm'].values[0]}"
        X_test = df[df.msoa11nm == msoa_nm].loc[:, "income_score":"metropolitan"]
        prediction_prob = f"There is a {str(round(logr_model.predict_proba(X_test)[0][1] * 100, 1))} % probability"
        prediction = logr_model.predict(X_test)[0]
        disabled = True
        if prediction == 1:
            the_text = "This area is LIKELY to have a charge point"
        else:
            the_text = "This area is NOT LIKELY to have a charge point"

    return the_text, msoa_description, lad_description, prediction_prob, disabled


@app.callback(
    [Output('submit-button', 'n_clicks'),
     Output('postcode', 'value'), Output('local_a', 'value')], [Input('reset-button', 'n_clicks')])
def reset(value):
    url = "http://api.postcodes.io/random/postcodes"
    f = requests.get(url).json()
    if value > 0:
        value = 0
    return value, f['result']['postcode'], [f['result']['admin_district']]


@app.callback(Output('text1', 'children'), [Input('var1', 'value')])
def definitions(value):
    return data_diction[value]


@app.callback(Output('text2', 'children'), [Input('var2', 'value')])
def definitions(value):
    return data_diction[value]


@app.callback(Output('map', 'srcDoc'),
              [Input('local_a', 'value'),
               Input('var2', 'value'),
               Input('postcode', 'value'),
               Input('submit-button', 'n_clicks')])
def remap(area, target, postcode, clicks):
    if clicks > 0:
        url = "https://api.postcodes.io/postcodes/" + postcode
        f = requests.get(url).json()
        lat = f['result']['latitude']
        long = f['result']['longitude']

        plot_area(df, target, lat, long, *area)
    return open('search.html', 'r').read()


@app.callback(Output('corr_graph', 'figure'), [
    Input('var1', 'value'),
    Input('var2', 'value'),
    Input('local_a', 'value'),
    Input('log_y_scale', 'value'),
    Input('log_x_scale', 'value')
])
def plot_corr(x_value, y_value, lad_name, y_scale, xscale):
    if len(lad_name) > 1:
        chart_text = "Multiple Local Authorities"
    else:
        chart_text = lad_name[0]

    fig = go.Figure(data=[
        go.Scatter(x=df[x_value],
                   y=df[y_value],
                   mode='markers',
                   name='Entire UK',
                   opacity=0.7,
                   marker=go.scatter.Marker(color='red',
                                            size=4,
                                            line=dict(width=0.5,
                                                      color='black'))),
        go.Scatter(
            x=df[df['lad13nm'].str.contains('|'.join(lad_name))][x_value],
            y=df[df['lad13nm'].str.contains('|'.join(lad_name))][y_value],
            text=chart_text,
            name='Local Authorities Selected',
            mode='markers',
            opacity=1,
            marker=go.scatter.Marker(color='green',
                                     size=6,
                                     line=dict(width=0.5, color='black')))
    ],
        layout=go.Layout(xaxis={
            'type': xscale,
            'title': x_value
        },
            yaxis={
                'type': y_scale,
                'title': y_value
            },
            margin={
                'l': 40,
                'b': 30,
                't': 20,
                'r': 20
            },
            legend={
                'x': 0,
                'y': 1
            },
            hovermode='closest'))
    fig.update_layout(template='plotly')
    return fig


if __name__ == "__main__":
    app.run_server(port=7050, debug=True)
