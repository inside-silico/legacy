# -*- coding: utf-8 -*-
"""SFFT-V1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bVqXZVSKVmKerb_OmbFqgcozeC6oNwxI

# Step Fall Financial Tools es una recopilacion de distintas herramientas para el analisis de activos, enfocadas en el mercado Argentino.
"""



import pandas as pd
from datetime import datetime
from pytz import timezone
import requests
import re
import json
import numpy as np 
import datetime
class yahoo:
  def get_history(ticker,date_start,date_end):
    newyork_tz = timezone('America/New_York')
    var = date_start.split("-")
    var = list(map(int, var1))
    p1 = str(int(newyork_tz.localize(datetime.datetime(var1[0],var1[1],var1[2], 8, 0, 0)).timestamp()))
    var = date_start.split("-")
    var = list(map(int, var1))
    p1 = str(int(newyork_tz.localize(datetime.datetime(var1[0],var1[1],var1[2], 8, 0, 0)).timestamp()))
    url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={p1}&period2={p2}&interval=1d&events=history&includeAdjustedClose=true"
    df = pd.read_csv(url)
    return df

  def get_quotes(tickers):
        url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
        headers = {
                "Accept"  :  "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding"  :  "gzip, deflate, br",
                "Accept-Language"  :  "en-US,en;q=0.5",
                "Cache-Control"  :  "no-cache",
                "Connection"  :  "keep-alive",
                "DNT"  :  "1",
                "Host"  :  "query1.finance.Yahoo.com",
                "Pragma"  :  "no-cache",
                "Upgrade-Insecure-Requests"  :  "1",
                "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0"  }
        response = requests.get(url = url+tickers, headers = headers)
        status = response.status_code
        if status != 200:
            print ("Yahoo no retorno status=200:", status)
        result = json.loads(response.text)
        df = pd.DataFrame(result["quoteResponse"]["result"])
        columns=['symbol','bid', 'ask', 'last', 'high', 'low', 'change', 'volume', 'previousclose']
        filter_columns=["symbol",'bid', 'ask', "regularMarketPrice", "regularMarketDayHigh", "regularMarketDayLow", "regularMarketChangePercent", "regularMarketVolume", "regularMarketPreviousClose"]
        df = df[filter_columns].copy()
        df.columns = columns
        df.change=df.change/100
        return df

class ambito:
  def dolar_blue(start_date,end_date):
    url = "https://mercados.ambito.com//dolar/informal/historico-general/"

    start_date = start_date.split("-")
    start_date = list(map(int, start_date))
    start_date_str = str(start_date[2])+"-"+str(start_date[1])+"-"+str(start_date[0])
    end_date = end_date.split("-")
    end_date = list(map(int, end_date))
    end_date_str = str(end_date[2])+"-"+str(end_date[1])+"-"+str(end_date[0])
    req = requests.get(url+start_date_str+'/'+end_date_str)
    data = req.json()
    data2= np.array(data)
    df = pd.DataFrame(data2, columns = ['Fecha','Compra','Venta'])
    df = df.drop(labels=0, axis=0)
    df['Compra'] = df['Compra'].str.replace(",", ".").astype(float)
    df['Venta'] = df['Venta'].str.replace(",", ".").astype(float)
    for i in range(1,len(df)+1,1):
      var1=df.at[i,"Fecha"].split("-")
      var1 = list(map(int, var1))
      df.at[i, 'Fecha']= datetime.date(var1[2],var1[1],var1[0])
    df.sort_values(by=['Fecha'], inplace=True)
    df = df.drop_duplicates("Fecha")
    df=df.reset_index()
    df=df.drop(['index'],axis=1)
    return df

  def dolar_oficial(start_date,end_date):
    url = "https://mercados.ambito.com//dolar/oficial/historico-general/"

    start_date = start_date.split("-")
    start_date = list(map(int, start_date))
    start_date_str = str(start_date[2])+"-"+str(start_date[1])+"-"+str(start_date[0])
    end_date = end_date.split("-")
    end_date = list(map(int, end_date))
    end_date_str = str(end_date[2])+"-"+str(end_date[1])+"-"+str(end_date[0])
    req = requests.get(url+start_date_str+'/'+end_date_str)
    data = req.json()
    data2= np.array(data)
    df = pd.DataFrame(data2, columns = ['Fecha','Compra','Venta'])
    df = df.drop(labels=0, axis=0)
    df['Compra'] = df['Compra'].str.replace(",", ".").astype(float)
    df['Venta'] = df['Venta'].str.replace(",", ".").astype(float)
    for i in range(1,len(df)+1,1):
      var1=df.at[i,"Fecha"].split("-")
      var1 = list(map(int, var1))
      df.at[i, 'Fecha']= datetime.date(var1[2],var1[1],var1[0])
    df.sort_values(by=['Fecha'], inplace=True)
    df = df.drop_duplicates("Fecha")
    df=df.reset_index()
    df=df.drop(['index'],axis=1)
    return df

  def dolar_solidario(start_date,end_date):
    url= "https://mercados.ambito.com//dolarturista/historico-general/"

    start_date = start_date.split("-")
    start_date = list(map(int, start_date))
    start_date_str = str(start_date[2])+"-"+str(start_date[1])+"-"+str(start_date[0])
    end_date = end_date.split("-")
    end_date = list(map(int, end_date))
    end_date_str = str(end_date[2])+"-"+str(end_date[1])+"-"+str(end_date[0])
    req = requests.get(url+start_date_str+'/'+end_date_str)
    data = req.json()
    data2= np.array(data)

    df = pd.DataFrame(data2, columns = ['Fecha','Venta'])
    df = df.drop(labels=0, axis=0)
    df['Venta'] = df['Venta'].str.replace(",", ".").astype(float)

    for i in range(1,len(df)+1,1):
      var1=df.at[i,"Fecha"].split("-")
      var1 = list(map(int, var1))
      df.at[i, 'Fecha']= datetime.date(var1[2],var1[1],var1[0])
    df.sort_values(by=['Fecha'], inplace=True)
    df = df.drop_duplicates("Fecha")
    df=df.reset_index()
    df=df.drop(['index'],axis=1)
    return df


class rava:
  def get_history(ticker,start_date,end_date):
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
      "especie": ticker, #Ticker
      "fecha_inicio": start_date, #Para que traiga todo
      "fecha_fin": end_date#Para que traiga todo
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
    quots.rename({'cierre': 'close','fecha':'date','apertura':'open','maximo':'high','minimo':'low','volumen':'volume'}, axis=1, inplace=True)
    quots=quots.drop(['especie'],axis=1)
    return quots