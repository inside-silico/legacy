#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Home Broker API - Market data downloader
# https://github.com/crapher/pyhomebroker.git
#
# Copyright 2020 Diego Degese
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from pyhomebroker import HomeBroker
import pandas as pd
import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import time
import datetime
from datetime import date
from sqlalchemy import create_engine
import pymysql
error=0

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="",
                               pw="",
                               db=""))



scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file=' ')
sh = gc.open('TestUpdate')

firtRun_bluechips=0
firtRun_galpones=0
firtRun_CEDEAR=0 
firtRun_bonds=0 
firtRun_ON=0  
firtRun_options=0
firtRun_repos=0


bluechips_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
bluechips_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
galpones_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
galpones_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
CEDEAR_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
CEDEAR_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
bonds_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
bonds_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
ON_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
ON_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
options_dF = pd.DataFrame(columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last",
                                       "change", "open", "high", "low", "previous_close", "turnover", "volume",
                                       'operations', 'datetime'])
options_dF[["ask","bid","change", "open", "high", "low", "previous_close","datetime"]].astype(float)
repos_dF = pd.DataFrame(columns=['symbol','settlement','days','bid_amount','bid_rate','ask_rate','ask_amount','last','change','open','high',  'low', 'previous_close','turnover','volume','operations','datetime'])


def example_online():

    broker = ""
    dni = ""
    user = ""
    password = ""

    hb = HomeBroker(int(broker), 
        on_open=on_open, 
        on_personal_portfolio=on_personal_portfolio, 
        on_securities=on_securities, 
        on_options=on_options, 
        on_repos=on_repos, 
        on_order_book=on_order_book, 
        on_error=on_error, 
        on_close=on_close)
        
    hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)
    
    hb.online.connect()
    hb.online.subscribe_securities('cedears','spot')
    hb.online.subscribe_securities('government_bonds','spot')
    hb.online.subscribe_options()

    now = time.strftime("%H")

    while now!="17":
        global bluechips_dF
        global galpones_dF
        global CEDEAR_dF
        global bonds_dF
        global ON_dF
        global options_dF
        global repos_dF
        print("cedear_df")
        sh = gc.open('Arb_Sheet')
        wks = sh.worksheet_by_title("CEDEAR_CI")
        wks.set_dataframe(CEDEAR_dF,(1,1), copy_index=True)
        time.sleep(3.7)
        print("bonds_df")
        sh = gc.open('Arb_Sheet')
        wks = sh.worksheet_by_title("Bonos_CI")
        wks.set_dataframe(bonds_dF,(1,1), copy_index=True)
        time.sleep(3.7)
        sh = gc.open('OpcionesWebapp')
        wks = sh.worksheet_by_title("Cotizaciones")
        wks.set_dataframe(options_dF,(1,1), copy_index=True)
        thisDataOp=options_dF
        thisDataOp =thisDataOp.reset_index()
        thisDataOp.to_sql("options", con = engine, if_exists = 'replace', chunksize = 1000)
        print("options_dF")
        time.sleep(2.2)
        now = time.strftime("%H")

    hb.online.unsubscribe_options()
    hb.online.unsubscribe_securities('cedears','ci')
    hb.online.unsubscribe_securities('government_bonds','ci')
    hb.online.disconnect()

def on_open(online):
    
    print('=================== CONNECTION OPENED ====================')

def on_personal_portfolio(online, portfolio_quotes, order_book_quotes):
    
    print('------------------- Personal Portfolio -------------------')
    print(portfolio_quotes)
    print('------------ Personal Portfolio - Order Book -------------')
    print(order_book_quotes)

def on_securities(online, quotes):

    var = quotes.iloc[2]['group']
    global bluechips_dF
    global galpones_dF
    global CEDEAR_dF
    global bonds_dF
    global ON_dF
    global firtRun_bluechips
    global firtRun_galpones
    global firtRun_ON
    global firtRun_CEDEAR
    global firtRun_bonds
    if var == 'bluechips':
        if firtRun_bluechips ==0:
            bluechips_dF=quotes
            firtRun_bluechips = 1
        else:
            bluechips_dF.update(quotes)        	
    if var == 'cedears':
        if firtRun_CEDEAR ==0:
            CEDEAR_dF=quotes
            firtRun_CEDEAR  = 1
        else:
            CEDEAR_dF.update(quotes)
    		        	
    if var == 'government_bonds':
        if firtRun_bonds == 0:
            bonds_dF=quotes
            firtRun_bonds = 1
        else:
            bonds_dF.update(quotes)
    		  
    if var == 'corporate_bonds':
        if firtRun_ON ==0:
            ON_dF=quotes
            firtRun_ON = 1
        else:
            ON_dF.update(quotes)
        	
def on_options(online, quotes):
    global options_dF
    global firtRun_options
    if firtRun_options ==0:
            options_dF=quotes
            firtRun_options  = 1
    else:
            options_dF.update(quotes) 

def on_repos(online, quotes):
    global repos_dF
    global firtRun_repos
    if firtRun_repos ==0:
            repos_dF=quotes
            firtRun_repos  = 1
    else:
           repos_dF.update(quotes)

def on_order_book(online, quotes):
    
    print('------------------ Order Book (Level 2) ------------------')
    print(quotes)
    
def on_error(online, exception, connection_lost):
    #print('@@@@@@@@@@@@@@@@@@@@@@@@@ Error @@@@@@@@@@@@@@@@@@@@@@@@@@')
    #print(exception)
    error=error+1

def on_close(online):

    print('=================== CONNECTION CLOSED ====================')

if __name__ == '__main__':
    example_online()

