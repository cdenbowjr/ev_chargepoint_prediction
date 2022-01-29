from dash import dcc, html
import dash_bootstrap_components as dbc


def correlation_graph(dataframe):
    return html.Div([
        dcc.Graph(id='corr_graph'),
        html.Div([
            dbc.RadioItems(id='log_y_scale',
                           options=[
                               {'label': 'Logarithmic y-axis', 'value': 'log'},
                               {'label': 'Linear y-axis scale', 'value': 'linear'}
                           ],
                           value='linear', className='mt-1',
                           style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'})
        ], className="mt-1",
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div([
            dbc.RadioItems(id='log_x_scale',
                           options=[
                               {'label': 'Logarithmic x-axis', 'value': 'log'},
                               {'label': 'Linear x-axis scale', 'value': 'linear'}
                           ],
                           value='linear')], className="mt-1",
            style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

        html.Div(id='feature-target', children=
        [
            html.Div(id='feature-variable', children=[
                dbc.Label("Feature Variable", size="lg"),
                dcc.Dropdown(id='var1',
                             value='total_netb4hsing',
                             options=[{
                                 'label': x,
                                 'value': x
                             } for x in dataframe.columns[4:]]
                             ),
                html.Div(id='text1', children='...waiting')
            ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div(id='divider', style={'width': '10%', 'display': 'inline-block', 'vertical-align': 'top'}),
            html.Div(id='target-variable', children=[
                dbc.Label("Target Variable", size="lg"),
                dcc.Dropdown(id='var2',
                             value='charge_points',
                             options=[{
                                 'label': x,
                                 'value': x
                             } for x in dataframe.columns[4:]]),
                html.Div(id='text2', children='...waiting')

            ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'})

        ], className="mt-4"),
    ],
        style={
            'width': '50%',
            'display': 'inline-block'
        })


def geographic_map(rand_postcode, rand_district, list_of_local_authorities):
    return html.Div([
        html.Iframe(id='map',
                    srcDoc=open('search.html', 'r').read(),
                    width='100%',
                    height='500px'),
        dcc.Dropdown(
            id='local_a', value=[rand_district], options=list_of_local_authorities, multi=True, className="mt-1"),
        # central_london+greater_london
        html.H4("Enter your post code here"),
        html.Div(id='postcode-input', children=[
            dbc.Input(id="postcode",
                      value=rand_postcode,
                      size="sm",
                      className="mt-4",
                      disabled=False,
                      style={'width': '50%', 'display': 'inline-block'}),
            dbc.Button(id='submit-button', className="mt-1", n_clicks=0, children='Submit'),
            dbc.Button(id='reset-button', className="mt-1", n_clicks=0, children='Reset')],
                 style={'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),
        html.Div(id='model-result', children=[
            html.Div(id="lad_loc", children="No Local Authority"),
            html.Div(id="msoa_loc", children="No MSOA"),
            html.Div(id="result", children="No result"),
            html.Div(id="prob", children="No probability")
        ], style={'width': '50%', 'display': 'inline-block'})
    ],
        style={
            'width': '50%',
            'float': 'right',
            'display': 'inline-block'
        })