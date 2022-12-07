import dash
from dash.dependencies import Input, Output
from dash import html
from dash import dcc
import plotly.graph_objs as go 
from datetime import date
import requests
import math

from sfft_v1 import *
import pandas as pd
import datetime

dolar_selected="oficial"


app = dash.Dash(__name__,suppress_callback_exceptions=True)

server = app.server
index_layout = html.Div( [ html.H3('Escribi bien salame')   ])
app.layout = html.Div(dcc.Location(id="url", refresh=True),id="page-content")



def VHC_graph():
  df=pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vRHQoXU18jm_yq8TFf04N6TKDjPRK1A3Iyvqte7JWSYV2g07BITTy0Ta4ZmxZRI7ICUsrPJ7W681O0E/pub?gid=640336420&single=true&output=csv")
  print(df)
  df.IV=df.IV.astype(float)
  df.Dias=df.Dias.astype(int)
  df=df.assign(HV =0.0)
  df.set_index("date",inplace=True)

  s = requests.Session()

  def strbetw(text, left, right):
    match = re.search( left + '(.*?)' + right, text)
    if match:  
      return match.group(1)
    return ''

    
  url = "https://www.rava.com"

  headers = {
      "Host" : "www.rava.com",
      "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
      "Accept-Language" : "en-US,en;q=0.5",
      "Accept-Encoding" : "gzip, deflate, br",    
      "DNT" : "1",
      "Connection" : "keep-alive",      
      "Upgrade-Insecure-Requests" : "1",
      "Sec-Fetch-Dest" : "document",
      "Sec-Fetch-Mode" : "navigate",
      "Sec-Fetch-Site" : "none",
      "Sec-Fetch-User" : "?1"
      }

  response = s.get(url = url, headers = headers)
  status = response.status_code
  if status != 200:
    print("login status", status)  
    exit()

  access_token = strbetw(response.text, ":access_token=\"\'", "\'\"")


  url = "https://clasico.rava.com/lib/restapi/v3/publico/cotizaciones/historicos"

  data = {
    "access_token": access_token, # - Parece que dura 30 minutos 
    "especie": "GGAL", #Ticker
    "fecha_inicio": "2021-06-01", #Para que traiga todo
    "fecha_fin": "2030-01-01"#Para que traiga todo
  }

  headers = {
      "Host" : "clasico.rava.com",
      "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
      "Accept" : "*/*",
      "Accept-Language" : "en-US,en;q=0.5",
      "Accept-Encoding" : "gzip, deflate",
      "Content-Type" : "application/x-www-form-urlencoded",
      "Origin" : "https://datos.rava.com",
      "DNT" : "1",
      "Connection" : "keep-alive",
      "Referer" : "https://datos.rava.com/",    
      "Sec-Fetch-Dest" : "empty",
      "Sec-Fetch-Mode" : "cors",
      "Sec-Fetch-Site" : "same-site"    
  }

  response = s.post(url = url, headers = headers, data = data)
  status = response.status_code
  if status != 200:
    print("form status", status)
    exit()
  quots=(pd.DataFrame(json.loads(response.text)['body']))
  quots.rename({'cierre': 'close','fecha':'date'}, axis=1, inplace=True)
  quots.date=pd.to_datetime(quots.date)
  print(quots)

  data = pd.DataFrame(quots['close'])
  data=data.assign(ROC =0.0)
  data=data.assign(F =0.0)
  data=data.rename(columns={"F":"date"})
  data.date=quots[["date"]].copy()
  data=data.assign(DL =0.0)
  data.DL=datetime.datetime(2022,4,13,0,0)-data.date
  data.DL=data.DL.dt.days.copy()
  data.loc[0]['ROC'] = 0

  for i in range(1,len(data)):
      var = math.log(((data.at[(i),'close'])) / (data.at[(i-1),'close']))
      data.loc[i]= [data.at[i,"close"],var,data.at[i,"date"],data.at[i,"DL"]]

  data=data.assign(HV =0.0)
  for i in range(39,len(data)):
    df_aux=pd.DataFrame()
    df_aux=df_aux.assign(F =0.1)
    df_aux.columns=['ROC']
    if data.at[i,"DL"] >40:
      var=39
    else:
      var=data.at[i,"DL"]-1
    for j in range(var,-1,-1):
      index=i-j
      df_aux.loc[j]=data.at[index,"ROC"]
    aux=df_aux.std()*(math.sqrt(262))
    data.loc[i]= [data.at[i,"close"],data.at[i,"ROC"],data.at[i,"date"],data.at[i,"DL"],aux]

  df_VHC=data
  df_VHC.date=df_VHC.date.dt.strftime("%Y-%m-%d")
  df_VHC.set_index("date", inplace=True)

  df.update(df_VHC)
  df.tail(30)
  df.reset_index(inplace=True)

  fig = go.Figure()
  
  fig.add_trace(go.Scatter(x=df.date, y=df.HV,name="HVC"))
  fig.add_trace(go.Scatter(x=df.date, y=df.IV,name="IV",line=dict(width=2,color='#FFC639')))
  fig.update_layout(template="plotly_dark")
  fig.update_layout(plot_bgcolor="#18191B",paper_bgcolor="#18191B")
  
  return fig





all_options = {
    'Dolar Oficial','Dolar Blue','Dolar Solidario'
}
page3 = html.Div([
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
    Output('display-selected-values', 'children'),
    Input('dolar_selected', 'value')
)
def set_display_childre(value):
    title_selected="dd"
    df=pd.DataFrame()
    if value=="Dolar Oficial":
        df= ambito.dolar_oficial("2020-03-01",date.today().strftime("%Y-%m-%d"))
        title_selected="Dolar Oficial"
        bad_value=datetime.date(2021,8,18)
        df =df.query("Fecha != @bad_value")

    if value=="Dolar Blue":
        df= ambito.dolar_blue("2020-03-01",date.today().strftime("%Y-%m-%d"))
        title_selected="Dolar Blue"
    if value=="Dolar Solidario":
        df= ambito.dolar_solidario("2020-03-01",date.today().strftime("%Y-%m-%d"))
        bad_value=datetime.date(2021,8,18)
        df =df.query("Fecha != @bad_value")
        title_selected="Dolar Solidario"
    
    trace = go.Scatter(x=list(df.Fecha), y=list(df.Venta))
    data = [trace]
    layout = dict(
        paper_bgcolor="#18191B",
        template="plotly_dark",
        plot_bgcolor="#18191B",

        title=title_selected,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                        label='1m',
                        step='month',
                        stepmode='backward'),
                    dict(count=6,
                        label='6m',
                        step='month',
                        stepmode='backward'),
                    dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate'),
                    dict(count=1,
                        label='1y',
                        step='year',
                        stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(visible = True),type='date'))

    fig = go.Figure(data=data, layout=layout)
    fig.update_yaxes(fixedrange=False,type="log")
    fig.update_xaxes(rangeselector_bgcolor="black")
    fig.update_traces(line=dict(width=2,color='yellow'))
    page =html.Div(children=[dcc.Graph(figure=fig)])
    return page


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname="/"):
    ctx = dash.callback_context
    triggered_by = ctx.triggered[0].get("prop_id")

    if pathname == "/dolar-blue":

        return page3

    elif pathname == "/vhc-ggal":

        return html.Div(children=[dcc.Graph(figure=VHC_graph())])

    else:
        return index_layout

if __name__ == "__main__":
    app.run_server(debug=True,host='0.0.0.0')
