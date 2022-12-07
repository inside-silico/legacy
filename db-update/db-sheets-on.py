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
sh = gc.open('ON_DB')
wks = sh.worksheet_by_title("ON_AUX")
print('=================== CONNECTION OPENED ====================')
tickers = pd.DataFrame(wks.get_values('A2','A310'))
new_sheet=0
today = date.today()
for i in range(len(tickers)):
	try:
		wks2 = sh.worksheet_by_title(tickers.at[i,0])
		#Peticion de Historicos a HomeBroker
		data = hb.history.get_daily_history(tickers.at[i,0], datetime.date(2010,1, 1), today)
		wks2.set_dataframe(data,(1,1), copy_head = True)
		data=data.set_index('date')
		data=data.assign(F =1)
		data.to_sql(tickers.at[i,0], con = engine, if_exists = 'replace', chunksize = 1000)
		print(tickers.at[i,0])
		time.sleep(0.3)

	except:
		sh.add_worksheet(tickers.at[i,0])
		wks2 = sh.worksheet_by_title(tickers.at[i,0])
		wks2.update_value('L1','=ArrayFormula(max(if(len(B:B),row(B:B),)))')
		wks2.update_value('M1','=indirect(ADDRESS(L1,1,3))')
		#Peticion de Historicos a HomeBroker
		data = hb.history.get_daily_history(tickers.at[i,0], datetime.date(2010,1, 1), today)
		wks2.set_dataframe(data,(1,1), copy_head = True)
		data=data.set_index('date')
		data=data.assign(F =1)
		data.to_sql(tickers.at[i,0], con = engine, if_exists = 'replace', chunksize = 1000)
		print("Added"+tickers.at[i,0])
		new_sheet=1
		time.sleep(1.4)

if(new_sheet==1):
	AUXforms=pd.DataFrame(columns=["Tickers","LastKnownDate","LastKnownValue"])
	AUXforms["Tickers"]=tickers[0]
	AUXforms["LastKnownDate"]="="+AUXforms["Tickers"]+"!M1"
	for i in range(len(AUXforms)):
		cell=i+2
		cell=str(cell)
		AUXforms.at[i,"LastKnownValue"] = "=VLOOKUP(B"+cell+","+tickers.at[i,0]+"!A:F,5,false)"
	AUXforms.set_index("Tickers",inplace=True)
	wks.set_dataframe(AUXforms,(1,2), copy_head = True)
	

print('=================== CONNECTION CLOSED ====================')
stoday = today.strftime("%d/%m/%Y")
#print("Last Update " + stoday)


