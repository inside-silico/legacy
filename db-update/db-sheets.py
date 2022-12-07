 
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
from pyhomebroker import HomeBroker
from sqlalchemy import create_engine
import pymysql
import time

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
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
gc = pygsheets.authorize(service_file='')

print("Enter the void")
#Conexion a HomeBroker
hb = HomeBroker(int(broker))
hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)
#Conexion a Google Console
sh = gc.open('Merval_DB')
wks = sh.worksheet_by_title("Dashboard")
today = date.today()
print('=================== CONNECTION OPENED ====================')
j=2
while j < 72: #Lectura de tickers de la Hoja Dashboard
	tickerT = wks.get_value((j,1))
	wks2 = sh.worksheet_by_title(tickerT)
	#Peticion de Historicos a HomeBroker
	data = hb.history.get_daily_history(tickerT, datetime.date(2017,1, 1), today)
	wks2.set_dataframe(data,(2,1), copy_head = False)
	data=data.set_index('date')
	data=data.assign(F =1)
	data.to_sql(tickerT, con = engine, if_exists = 'replace', chunksize = 1000)
	print(tickerT)
	j += 1
	time.sleep(1)
print('=================== CONNECTION CLOSED ====================')
stoday = today.strftime("%d/%m/%Y")
print("Last Update " + stoday)



