import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import numpy as np
import plotly.graph_objs as go
from pyhomebroker import HomeBroker
from open_chori import *


db_host=""
db_pass=""
db_usr=""

openBYMAdata.connect()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

def graph_history(ticker):
    
    today = datetime.date.today()
    broker = 
    dni = ''
    user = ''
    password = ''
    hb = HomeBroker(int(broker))
    hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)

    df=hb.history.get_daily_history(ticker, datetime.date(2002,1, 1), today)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.date, y=df.close,name="IV",line=dict(width=2,color='#FFC639')))
    fig.update_layout(template="plotly_dark")
    fig.update_layout(plot_bgcolor="#18191B",paper_bgcolor="#18191B")
    
    return fig


available_indicators=['IRC1D',"VSC1D","VSC2D","DICAD","DICA","OCR14","CS8HO","ODNM1","OIRX6","GGAL","SPBYCAP"]
app.layout = html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='ticker_selected',
                        options=[{'label': i, 'value': i} for i in available_indicators],
                        value='AL30'
                    ),
                ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'}),
            ]),
            html.Div([
                dcc.Graph(id='quots_graph'),

            ],style={"padding-top":"50px"}),

        ])

@app.callback(
    dash.dependencies.Output('quots_graph', 'figure'),
    dash.dependencies.Input('ticker_selected', 'value'))
def update_graph(ticker_selected):
    return graph_history(ticker_selected)


if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0')
