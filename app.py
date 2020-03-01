import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import json
from shapely.geometry import Polygon
import folium
from src.functions import functions_for_project as ffp
from src.data import data_dictionary as data_d

msoa_uk = ffp.load_geojson(
    'http://www.data4apurpose.com/client_html'
    '/Middle_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BFC_ultra_simple.geojson')

df = pd.read_csv('http://www.data4apurpose.com/client_html/full_processed_data.csv')
central_london = ['City of London', 'Camden', 'Greenwich', 'Hackney', 'Hammersmith and Fulham', 'Islington',
                  'Kensington and Chelsea', 'Lambeth', 'Lewisham', 'Southwark', 'Tower Hamlets', 'Wandsworth',
                  'Westminster']

# scaler = StandardScaler()
# chrg_select = pd.DataFrame(ppf.ColumnSelector('charge_points').fit_transform(df).values.reshape(-1,1))
# df['charge_points'] = ppf.FeatureLogTransform().fit_transform(chrg_select)


df = pd.merge(df, msoa_uk, left_on='msoa11cd', right_on='properties.msoa11cd')

lad = [{'label': area, 'value': area} for area in df.lad13nm.unique()]

data_diction = data_d.EV_britain().description


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

        with open('search.geojson', 'w') as json_file:
            json.dump(search_area_json, json_file)

        start_lat = search_area.apply(centroid_calc, axis=1).apply(lambda x: x[0]).mean()
        start_lon = search_area.apply(centroid_calc, axis=1).apply(lambda x: x[1]).mean()

        area_map = folium.Map(location=(start_lat, start_lon), zoom_start=11)

        area_map.choropleth(geo_data='search.geojson', data=search_area,
                            columns=["properties.msoa11cd", feature_var],
                            key_on='feature.properties.msoa11cd', fill_color='Spectral_r', highlight=True, name="areas",
                            legend_name=data_d.EV_britain().description[feature_var])

        folium.LayerControl().add_to(area_map)
        area_map.save("search.html")

    except:
        print("This is not a council area in London")


# print(data_d.EV_britain().description["income_score"])
# print(plot_area(merged_df,"crime_score","Southwark"))


app = dash.Dash('__name__')
server = app.server

app.layout = html.Div([html.Div(
    [html.H1('Correlations'),
     dcc.Graph(id='graph'),
     html.H3('Feature'),
     dcc.Dropdown(id='var1', value='income_score', options=[{'label': x, 'value': x} for x in df.columns[4:]]),
     html.Div(id='text1', children='...waiting'),
     html.H3('Target Variable'),
     dcc.Dropdown(id='var2', value='charge_points', options=[{'label': x, 'value': x} for x in df.columns[4:]]),
     html.Div(id='text2', children='...waiting')
     ], style={'width': '50%', 'display': 'inline-block'}),

    html.Div(
        [html.H1("Mapping"),
         html.Iframe(id='map', srcDoc=open('search.html', 'r').read(), width='100%', height='500px'),
         dcc.Dropdown(id='local_a', value=central_london, options=lad, multi=True)
         ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
]
)


@app.callback(Output('text1', 'children'), [Input('var1', 'value')])
def definitions(value):
    return data_diction[value]
    # return value


@app.callback(Output('text2', 'children'), [Input('var2', 'value')])
def definitions(value):
    return data_diction[value]
    # return value


@app.callback(Output('map', 'srcDoc'), [Input('local_a', 'value'), Input('var2', 'value')])
def remap(area, target):
    plot_area(df, target, *area)
    # print(*area,target)
    return open('search.html', 'r').read()


@app.callback(Output('graph', 'figure'),
              [Input('var1', 'value'), Input('var2', 'value'), Input('local_a', 'value')])
def clean_data(x_value, y_value, ladname):
    # print(df[value2])
    return {
        'data': [
            dict(
                x=df[x_value],
                y=df[y_value],
                # text=merged_df[merged_df['lad13nm'] == i]['metropolitan'],
                name='Entire UK',
                mode='markers',
                opacity=0.7,
                marker={
                    'color': 'red',
                    'size': 4,
                    'line': {'width': 0.5, 'color': 'black'}
                },

            ),
            dict(
                x=df[df['lad13nm'].str.contains('|'.join(ladname))][x_value],
                y=df[df['lad13nm'].str.contains('|'.join(ladname))][y_value],
                # text=merged_df[merged_df['lad13nm'] == i]['metropolitan'],
                name = 'Local Authorities Selected',
                mode='markers',
                opacity=1,
                marker={
                    'color': 'green',
                    'size': 6,
                    'line': {'width': 0.5, 'color': 'black'}
                },

            )
        ],
        'layout': dict(
            xaxis={'type': 'linear', 'title': x_value},
            yaxis={'type': 'linear', 'title': y_value},
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
    # webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=True)
