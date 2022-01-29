from dash import html
import dash_bootstrap_components as dbc

navbar_style = [dbc.themes.MORPH]  # MATERIA,
EV_LOGO_IMAGE1 = "https://freesvg.org/img/Chrisdesign-Beetle-car.png"
EV_LOGO_IMAGE2 = "https://freesvg.org/img/eco_green_energy_C.png"

car_logo = dbc.Col(html.Img(src=EV_LOGO_IMAGE1, height=75, width=150,
                            style={'display': 'float', 'object-fit': 'cover',
                                   'margin-left': "50px", 'margin-right': "50px"}
                            ))
charge_logo = dbc.Col(html.Img(src=EV_LOGO_IMAGE2, height=75, width=75
                               ))
dashboard_title = dbc.Col(dbc.NavbarBrand(html.H1("EV charge point Location Predictor"), className="ms-2"),
                          style={'display': 'float', 'object-fit': 'cover',
                                 'margin-left': "20px", 'margin-right': "50px"}
                          )

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dashboard_title, charge_logo, car_logo, charge_logo
                    ],
                    align="center",
                    className="g-0"
                ),
                href="https://www.google.com",
                style={"textDecoration": "none"}
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        ],
        fluid=True
    ),
    color="#FFFFFF",
    dark=False,
)
