import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import pandas as pd
import datetime
from datetime import date
import requests
import numpy as np

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')
sh = gc.open('Dolar-Blue')
today = date.today()
stoday = today.strftime("%d-%m-%Y")
start_date="01-01-2021"

url = ["https://mercados.ambito.com//dolar/oficial/historico-general/","https://mercados.ambito.com//dolar/informal/historico-general/"]
shDolar=['DatosOficial','Datos']
rangeCell=[4607,4711]
for i in range(len(url)):
    req = requests.get(url[i]+start_date+'/'+stoday)
    data = req.json()
    data2= np.array(data)
    df = pd.DataFrame(data2, columns = ['Fecha','Compra','Venta'])
    df = df.drop(labels=0, axis=0)
    df=df.drop_duplicates("Fecha")
    #df['Compra'] = df['Compra'].str.replace(",", ".").astype(float)
    #df['Venta'] = df['Venta'].str.replace(",", ".").astype(float)
    #df['Fecha']=pd.to_datetime(df['Fecha'])
    df = df.sort_index(ascending=False)
    wks2 = sh.worksheet_by_title(shDolar[i])
    wks2.set_dataframe(df,(rangeCell[i],1), copy_index=False, copy_head=False)
    print(df)
