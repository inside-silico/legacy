import os
import re
import json
import pandas as pd
import requests
import numpy as np
import plotly.graph_objs as go 
import datetime
import math


def VHC_graph():
  df=pd.read_csv(" ")
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

  data = pd.DataFrame(quots['close'])
  data=data.assign(ROC =0.0)
  data=data.assign(F =0.0)
  data=data.rename(columns={"F":"date"})
  data.date=quots[["date"]].copy()
  data=data.assign(DL =0.0)
  data.DL=datetime.datetime(2021,12,17,0,0)-data.date
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
