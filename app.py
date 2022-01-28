#!/usr/bin/env python
# coding: utf-8
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import joblib
import requests

import pandas as pd
from src.production.plotting import load_geojson, plot_area
from src.data import data_dictionary as data_d

# PULL DATA BLOCK
df = pd.read_csv(
    'http://www.data4apurpose.com/client_html/full_processed_data.csv')

# PULL GEODATA BLOCK
msoa_uk = load_geojson(
    'http://www.data4apurpose.com/client_html'
    '/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_ultra_simple.geojson'
)

data_diction = data_d.EV_britain().description

central_london = [
    'City of London', 'Camden', 'Greenwich', 'Hackney',
    'Hammersmith and Fulham', 'Islington', 'Kensington and Chelsea', 'Lambeth',
    'Lewisham', 'Southwark', 'Tower Hamlets', 'Wandsworth', 'Westminster'
]

greater_london = [
    'Croydon', 'Sutton', 'Brent', 'Ealing', 'Hounslow', 'Richmond', 'Kingston',
    'Merton', 'Bromley', 'Bexley', 'Havering', 'Barking and Dagenham',
    'Redbridge', 'Newham', 'Waltham Forest', 'Haringey', 'Enfield', 'Barnet',
    'Harrow', 'Hillingdon'
]

lad = [{'label': area, 'value': area} for area in df.lad13nm.unique()]

logr_model = joblib.load('./models/logistic_regression_model')

df = pd.merge(df, msoa_uk, left_on='msoa11cd', right_on='properties.msoa11cd')

random_url = "http://api.postcodes.io/random/postcodes"
random_request = requests.get(random_url).json()['result']
random_postcode, random_district = random_request['postcode'], random_request['admin_district']

app = dash.Dash('__name__')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('Predicting EV charge points'),
        dcc.Graph(id='corr_graph'),
        html.Div([
            dcc.RadioItems(id='log_y_scale',
                           options=[
                               {'label': 'Logarithmic y-axis', 'value': 'log'},
                               {'label': 'Linear y-axis scale', 'value': 'linear'}
                           ],
                           value='linear'),
            dcc.RadioItems(id='log_x_scale',
                           options=[
                               {'label': 'Logarithmic x-axis', 'value': 'log'},
                               {'label': 'Linear x-axis scale', 'value': 'linear'}
                           ],
                           value='linear')]),
        html.H3('Feature'),
        dcc.Dropdown(id='var1',
                     value='total_netb4hsing',
                     options=[{
                         'label': x,
                         'value': x
                     } for x in df.columns[4:]]),
        html.Div(id='text1', children='...waiting'),
        html.H3('Target Variable'),
        dcc.Dropdown(id='var2',
                     value='charge_points',
                     options=[{
                         'label': x,
                         'value': x
                     } for x in df.columns[4:]]),
        html.Div(id='text2', children='...waiting')
    ],
        style={
            'width': '50%',
            'display': 'inline-block'
        }),
    html.Div([
        html.H1("Mapping"),
        html.Iframe(id='map',
                    srcDoc=open('search.html', 'r').read(),
                    width='100%',
                    height='500px'),
        dcc.Dropdown(
            id='local_a', value=[random_district], options=lad, multi=True),  # central_london+greater_london
        html.H3("Enter your post code here"),
        dcc.Input(id="postcode", value=random_postcode, disabled=False),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Button(id='reset-button', n_clicks=0, children='Reset'),
        html.Div(id="lad_loc", children="No Local Authority"),
        html.Div(id="msoa_loc", children="No MSOA"),
        html.Div(id="result", children="No result"),
        html.Div(id="prob", children="No probability")
    ],
        style={
            'width': '50%',
            'float': 'right',
            'display': 'inline-block'
        })
])


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

        # msoa = ffp.pcd_dict(pcd_dict)[value]
        msoa_description = f"This is in the MSOA: {df[df.msoa11nm == msoa_nm]['msoa11nm'].values[0]}"
        lad_description = f"This is in the Local Authority of {df[df.msoa11nm == msoa_nm]['lad13nm'].values[0]}"
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
        # print(*area,target)
    return open('search.html', 'r').read()


@app.callback(Output('corr_graph', 'figure'), [
    Input('var1', 'value'),
    Input('var2', 'value'),
    Input('local_a', 'value'),
    Input('log_y_scale', 'value'),
    Input('log_x_scale', 'value')
])
def plot_corr(x_value, y_value, lad_name, y_scale, xscale):
    # print(df[value2])
    return go.Figure(data=[
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
            text="ddd",
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


if __name__ == "__main__":
    app.run_server(port=7050, debug=False)
