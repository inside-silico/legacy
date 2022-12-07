import pandas as pd
import datetime
from datetime import date
import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import time
import numpy as np

today = date.today()
stoday = today.strftime("%Y-%m-%d")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')
sheetOut=gc.open("DB_Opciones")
sh=gc.open("Opciones")
wks = sh.worksheet_by_title("Cotizaciones")
last_quot=wks.get_value((3,22))
#last_quot=stoday
if last_quot==stoday:

    stocksSh=['COME','GGAL','YPFD',]
    for i in range(len(stocksSh)):
        wks = sh.worksheet_by_title(stocksSh[i]+"/TasaDB")
        quots = pd.DataFrame(wks.get_values('Q2','Z2'))
        time.sleep(2.7)
        wks = sheetOut.worksheet_by_title(stocksSh[i]+"/ATM")
        print(stocksSh[i]+"/ATM")
        lenghtRow= wks.get_value((1,12))
        lenghtRow=int(lenghtRow) + 1
        wks.set_dataframe(quots,(lenghtRow,1), copy_head = False)
        time.sleep(2.7)

