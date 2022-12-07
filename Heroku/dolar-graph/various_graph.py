import os
import plotly.graph_objs as go 

import dash
from dash import dcc
from dash import html
from dash import dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from layout import *
from layout_minimal import *

from functions import *

app = dash.Dash(__name__,suppress_callback_exceptions=True)

server = app.server

db_host=""
db_pass=""
db_usr=""




def mep_page():
    available_indicators=['AL29','AL30','AL35','GD29','GD30','GD35','AY24']
    page = html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='mep_ticker_selected',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='AL30'
                    ),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Div([
                dcc.Graph(id='mep_graph'),

            ],style={"padding-top":"50px"}),

        ])
    return page

all_options = {'Dolar Oficial','Dolar Blue','Dolar Solidario'}
dolar_page = html.Div([
    dcc.RadioItems(
        id='dolar_selected',
        options=[{'label': k, 'value': k} for k in all_options],
        value='Dolar Blue',
        style={'display': 'block','text-align':'center','color':'grey'}
    ),
    html.Hr(),
    html.Div(id='display-selected-values')
])

@app.callback(
    dash.dependencies.Output('display-selected-values', 'children'),
    dash.dependencies.Input('dolar_selected', 'value')
)
def set_display_childre(value):
    return graphics.dolar_ambito(value)

index_layout = html.Div( [ html.H3('Escribi bien salame')   ])
app.layout = html.Div(dcc.Location(id="url", refresh=True),id="page-content")

@app.callback(
    dash.dependencies.Output('mep_graph', 'figure'),
    dash.dependencies.Input('mep_ticker_selected', 'value'))
def update_graph(mep_ticker_selected):
    return graphics.mep_graph(mep_ticker_selected)




@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname="/"):
    ctx = dash.callback_context
    triggered_by = ctx.triggered[0].get("prop_id")

    if pathname == "/page3":

        page=html.Div([
                dcc.Graph(id='diff_par_graph'),

            ],style={"padding-top":"50px"})

        return page

    elif pathname == "/mep-GD30":

        return mep_page()
    elif pathname == "/exchange":

        return dolar_page

    elif pathname == "/brecha":
        page =html.Div(children=[dcc.Graph(figure=graphics.brecha())])
        return page

    
    else:
        return index_layout

if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0')
