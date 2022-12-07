  
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Home Broker API - Market data downloader
# https://github.com/crapher/pyhomebroker.git
# Copyright 2020 Diego Degese
# 
# Copyright 2021 Blue Light Analytics, Programed by Julio Gamarra.
#


import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import datetime
from datetime import date
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import pymysql
import time
from sfft_v1 import *

engine = create_engine("mysql+pymysql://{user}:{pw}@flame2/{db}"
                       .format(user="",
                               pw="",
                               db=""))
#=================== Credenciales HomeBroker ====================
broker = 
dni = ''
user = ''
password = ''

#=================== Crendenciales Google Console========
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='./client_secret.json')

print("Enter the void")


#Conexion a Google Console
sh = gc.open('Merval_DB2')
wks = sh.worksheet_by_title("Dashboard")
today = date.today()
print('=================== CONNECTION OPENED ====================')

tickers = pd.DataFrame(wks.get_values('A2','A310'))
data2= np.array(tickers[0])

for i in range(len(data2)):
	try:
		tickerT = data2[i]
		wks2 = sh.worksheet_by_title(tickerT)
		#Peticion de Historicos a HomeBroker
		data = rava.get_history(tickerT,"2021-01-01","2050-01-01")
		data=data.rename(columns={'timestamp': 'F'})
		data.to_sql(tickerT, con = engine, if_exists = 'replace', chunksize = 1000)
		print(tickerT)
	except:
		print("Check Ticker")
print('=================== CONNECTION CLOSED ====================')
stoday = today.strftime("%d/%m/%Y")
print("Last Update " + stoday)


