#!/usr/bin/env python
# coding: utf-8

# In[1]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import joblib

import pandas as pd
import json
from shapely.geometry import Polygon
import folium
from src.functions import functions_for_project as ffp
from src.data import data_dictionary as data_d
import numpy as np
import requests


# In[2]:


df = pd.read_csv(
    'http://www.data4apurpose.com/client_html/full_processed_data.csv')


# In[3]:


msoa_uk = ffp.load_geojson(
    'http://www.data4apurpose.com/client_html'
    '/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_ultra_simple.geojson'
)


# In[4]:


data_diction = data_d.EV_britain().description


# In[ ]:


#pcd_dict = pd.read_csv("./data/raw/geo_spatial/pcd_msoa.csv")


# In[5]:


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


# In[6]:


logr_model = joblib.load('./models/logistic_regression_model')


# In[7]:


df = pd.merge(df, msoa_uk, left_on='msoa11cd', right_on='properties.msoa11cd')


# In[14]:


app = dash.Dash('__name__')
server = app.server

app.layout = html.Div([
    html.Div([
        html.H1('Predicting EV charge points'),
        dcc.Graph(id='corr_graph'),
        html.Div([dcc.RadioItems(id='log_yscale',options=[{'label':'Logarithmic y-axis','value':'log'},
                                               {'label':'Linear y-axis scale','value':'linear'}],value='linear'),
        dcc.RadioItems(id='log_xscale',options=[{'label':'Logarithmic x-axis','value':'log'},
                                               {'label':'Linear x-axis scale','value':'linear'}],value='linear')]),
        html.H3('Feature'),
        dcc.Dropdown(id='var1',
                     value='total_netafterhsing',
                     options=[{
                         'label': x,
                         'value': x
                     } for x in df.columns[4:]]),
        html.Div(id='text1', children='...waiting'),
        html.H3('Target Variable'),
        dcc.Dropdown(id='var2',
                     value='2019_q2',
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
            id='local_a', value=["Tower Hamlets"], options=lad, multi=True),#central_london+greater_london
        html.H3("Enter your post code here"),
        dcc.Input(id="postcode",value="CR0 2GL",disabled=False),
        html.Button(id='submit-button', n_clicks=0, children='Submit'),
        html.Button(id='reset-button', n_clicks=0, children='Reset'),
        html.Div(id="lad_loc",children="No Local Authority"),
        html.Div(id="msoa_loc",children="No MSOA"),
        html.Div(id="result",children="No result"),
        html.Div(id="prob",children="No probability")
    ],
        style={
        'width': '50%',
                 'float': 'right',
                 'display': 'inline-block'
    })
])


# In[16]:


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
    url = "https://api.postcodes.io/postcodes/"+value
    f = requests.get(url).json()
    msoa_nm = f['result']['msoa']
    if clicks > 0:

        #msoa = ffp.pcd_dict(pcd_dict)[value]
        msoa_description = f"This is in the MSOA: {df[df.msoa11nm == msoa_nm]['msoa11nm'].values[0]}"
        lad_description = f"This is in the Local Authority of {df[df.msoa11nm == msoa_nm]['lad13nm'].values[0]}"
        X_test = df[df.msoa11nm == msoa_nm].loc[:, "income_score":"metropolitan"]
        prediction_prob = f"There is a {str(round(logr_model.predict_proba(X_test)[0][1]*100,1))} % probability"
        prediction = logr_model.predict(X_test)[0]
        disabled = True
        if prediction == 1:
            the_text = "This area is LIKELY to have a charge point"
        else:
            the_text = "This area is NOT LIKELY to have a charge point"

    return (the_text, msoa_description, lad_description, prediction_prob,disabled)


@app.callback(
    [Output('submit-button', 'n_clicks'),
     Output('postcode', 'value')], [Input('reset-button', 'n_clicks')])
def reset(value):
    if value > 0:
        value = 0
    
    return (0,"CR0 2GL")


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
def remap(area, target,postcode,clicks):
    if clicks > 0:
        
        url = "https://api.postcodes.io/postcodes/"+postcode
        f = requests.get(url).json()
        lat = f['result']['latitude']
        long = f['result']['longitude']

        ffp.plot_area(df, target,lat,long,*area)
        # print(*area,target)
    return open('search.html', 'r').read()


@app.callback(Output('corr_graph', 'figure'), [
    Input('var1', 'value'),
    Input('var2', 'value'),
    Input('local_a', 'value'),
    Input('log_yscale', 'value'),
    Input('log_xscale', 'value')
])
def plot_corr(x_value, y_value, ladname, yscale, xscale):
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
            x=df[df['lad13nm'].str.contains('|'.join(ladname))][x_value],
            y=df[df['lad13nm'].str.contains('|'.join(ladname))][y_value],
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
                                          'type': yscale,
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


# In[17]:


if __name__ == "__main__":
    # webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(port = 7050, debug=False)


# In[ ]:


# scaler = StandardScaler()
# chrg_select = pd.DataFrame(ppf.ColumnSelector('charge_points').fit_transform(df).values.reshape(-1,1))
# df['charge_points'] = ppf.FeatureLogTransform().fit_transform(chrg_select)

# print(data_d.EV_britain().description["income_score"])
# print(plot_area(merged_df,"crime_score","Southwark"))

