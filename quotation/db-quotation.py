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

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="",
                               pw="",
                               db=""))

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
galpones_dF = pd.DataFrame(columns=["symbol", 'settlement',"bid_size", "bid", "ask", "ask_size", "last",
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
                                       'operations', 'datetime','expiration','strike','kind','underlying_asset'])
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
    hb.online.subscribe_options()
    hb.online.subscribe_securities('general_board','48hs')
    hb.online.subscribe_repos()

    while True:
        global bluechips_dF
        global galpones_dF
        global CEDEAR_dF
        global bonds_dF
        global ON_dF
        global options_dF
        global repos_dF
        thisDataOp=options_dF
        thisDataOp =thisDataOp.reset_index()
        thisDataOp.to_sql("options", con = engine, if_exists = 'replace', chunksize = 1000)
        print("options_dF")
        time.sleep(5)
        thisData= repos_dF
        thisData= thisData.reset_index()
        thisData = thisData[['PESOS' in s for s in repos_dF.index]]
        thisData['settlement'] = pd.to_datetime(thisData['settlement'])
        thisData.to_sql("repos", con = engine, if_exists = 'replace', chunksize = 1000)
        print("repos")
        time.sleep(5)
        thisDataGlp= galpones_dF
        thisDataGlp['change'] = thisDataGlp["change"] / 100
        thisDataGlp['datetime'] = pd.to_datetime(thisDataGlp['datetime'])
        thisDataGlp =thisDataGlp.reset_index()
        thisDataGlp.to_sql("galpones", con = engine, if_exists = 'replace', chunksize = 1000)
        print("galpones_dF")
        time.sleep(5)

    hb.online.unsubscribe_securities('general_board','48hs')
    hb.online.unsubscribe_options()
    hb.online.unsubscribe_repos()
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
    if var == 'general_board':
        if firtRun_galpones ==0:
            galpones_dF=quotes
            firtRun_galpones  = 1
        else:
            galpones_dF.update(quotes)
    		        	
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

