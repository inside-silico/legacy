from datetime import date
from pyhomebroker import HomeBroker
from sqlalchemy import create_engine
import pygsheets
import pandas as pd
from oauth2client.service_account import  ServiceAccountCredentials
from SHD import *

gc = pygsheets.authorize(service_file='./client_secret.json')
today = date.today()
stoday = today.strftime("%Y-%m-%d")

sh = gc.open('Opciones')
wks = sh.worksheet_by_title("Cotizaciones")
engine = create_engine("mysql+pymysql://{user}:{pw}@flame2/{db}"
                       .format(user="",
                               pw="",
                               db=""))

host = ""  
broker=
dni = ""
user = ""
pas = ""

hb = HomeBroker(int(broker))
hb.auth.login(dni=dni, user=user, password=pas, raise_exception=True)
SHD.catcher_connect(host,dni,user,pas)

quots=SHD.get_options()
quots.change=quots.change/100

#quots.columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last","change", "open", "high", "low", "previous_close", "turnover", "volume",'operations', 'datetime','expiration','strike','kind','underlying_asset']
quotsCleaned = quots[quots["underlying_asset"].isin(['GGAL','YPFD','COME'])]
df2=quotsCleaned
df2=df2.drop(["bid_size", "bid", "ask", "ask_size",'expiration','strike','kind','underlying_asset'],axis=1)
df2["datetime"]= today
df2=df2.set_index("symbol")
df=df2
df1=df.reset_index()

last_quot=wks.get_value((3,22))
if last_quot==stoday:
        for i in range(len(df2)):
                try:
                        df= hb.history.get_intraday_history(df1.at[i,"symbol"])
                        try:
                                df.to_sql(df1.at[i,"symbol"], index=False, con = engine, if_exists = 'append', chunksize = 1000)
                        except:
                                df=df.assign(F =0.1)
                                df.to_sql(df1.at[i,"symbol"], index=False,con = engine, if_exists = 'replace', chunksize = 1000)
                except:
                        print("NoInfo at "+df1.at[i,"symbol"])
