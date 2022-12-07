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
from sqlalchemy import create_engine
import pymysql
error=0
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost:3307/{db}"
                       .format(user="",
                              pw="",
                              db=""))


oBonos2 = ['AE38D-48hs','AL29D-48hs','AL30D-48hs','AL35D-48hs','AL41D-48hs','GD29D-48hs','GD30D-48hs','GD35D-48hs','GD38D-48hs','GD41D-48hs','GD46D-48hs']
tickerUSD_dF = pd.DataFrame({'symbol' : oBonos2}, columns=["symbol","bid", "ask", "last"])
tickerUSD_dF[["ask","bid","last"]].astype(float)
tickerUSD_dF = tickerUSD_dF.set_index("symbol")


oBonos=['AE38-48hs','AL29-48hs','AL30-48hs','AL35-48hs','AL41-48hs','GD29-48hs','GD30-48hs','GD35-48hs','GD38-48hs','GD41-48hs','GD46-48hs']
tickerARS_dF = Bonos = pd.DataFrame({'symbol' : oBonos}, columns=["symbol", "bid", "ask", "last"])
tickerARS_dF[["ask","bid","last"]].astype(float)

tickerARS_dF = tickerARS_dF.set_index("symbol")

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
    hb.online.subscribe_securities('government_bonds','48hs')
    hb.online.subscribe_securities('government_bonds','spot')

    while True:
        global tickerARS_dF
        global tickerUSD_dF
        #print (tickerARS_dF)
        #print (tickerUSD_dF)
        thisData = tickerARS_dF
        thisData = thisData.reset_index()
        thisData.rename(columns={"symbol":"tickerARS","last":"lastARS"}, inplace=True)
        thisDF= tickerUSD_dF
        thisDF = thisDF.reset_index()
        thisDF.rename(columns={"symbol":"tickerUSD","last":"lastUSD"}, inplace=True)
        thisData=pd.concat([thisData,thisDF],axis=1)
        thisData['MEP48hs']=thisData['lastARS']/thisData['lastUSD']
        thisData['MEP48hs']=thisData['MEP48hs'].format('3.14', decimal.Decimal('3.14'))
        print(thisData)
        thisData.to_sql("mep", con = engine, if_exists = 'replace', chunksize = 1000)
        time.sleep(7)
        print("done")

    hb.online.unsubscribe_securities('government_bonds','spot')
    hb.online.unsubscribe_securities('government_bonds','48hs')
    hb.online.disconnect()

def on_open(online):
    
    print('=================== CONNECTION OPENED ====================')

def on_personal_portfolio(online, portfolio_quotes, order_book_quotes):
    
    print('------------------- Personal Portfolio -------------------')
    print(portfolio_quotes)
    print('------------ Personal Portfolio - Order Book -------------')
    print(order_book_quotes)

def on_securities(online, quotes):
    global tickerARS_dF
    global tickerUSD_dF
    thisData = quotes
    thisData = thisData.reset_index()
    thisData['symbol'] = thisData['symbol'] + '-' +  thisData['settlement']
    thisData = thisData.set_index("symbol")
    thisData = thisData.drop(["settlement", "change", "open", "high", "low", "previous_close", "turnover", "volume",'operations', 'datetime', "ask_size", "bid_size"], axis=1)
    tickerARS_dF.update(thisData)
    tickerUSD_dF.update(thisData)
        	
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
    print(exception)


def on_close(online):

    print('=================== CONNECTION CLOSED ====================')

if __name__ == '__main__':
    example_online()

