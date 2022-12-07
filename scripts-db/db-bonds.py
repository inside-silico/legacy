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
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

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
gc = pygsheets.authorize(service_file='')

#Conexion a HomeBroker
hb = HomeBroker(int(broker))
hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)
#Conexion a Google Console
print('=================== CONNECTION OPENED ====================')
sh = gc.open('Bonos_DB')
wks = sh.worksheet_by_title("Bonos_AUX")
tickers = pd.DataFrame(wks.get_values('A2','A310'))
new_sheet=0
today = date.today()
for i in range(len(tickers)):
	try:
		#Peticion de Historicos a HomeBroker
		data = hb.history.get_daily_history(tickers.at[i,0], datetime.date(2010,1, 1), today)
		data=data.assign(F = 1)
		data.to_sql(tickers.at[i,0], con = engine, if_exists = 'replace', chunksize = 1000)
		print(tickers.at[i,0])


	except:
		print("Check Tickers")

print('=================== CONNECTION CLOSED ====================')
stoday = today.strftime("%d/%m/%Y")
#print("Last Update " + stoday)

