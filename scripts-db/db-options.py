from sqlalchemy import create_engine
import pandas as pd
import datetime
from datetime import date
import pymysql
import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import time
import numpy as np
from SHD import *

today = date.today()
stoday = today.strftime("%Y-%m-%d")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')

engine = create_engine("mysql+pymysql://{user}:{pw}@flame2/{db}"
                       .format(user="",
                               pw="",
                               db=""))

sh = gc.open('OpcionesWebapp')
wks = sh.worksheet_by_title("Cotizaciones")

host = ""  
broker=
dni = ""
user = ""
pas = ""

SHD.catcher_connect(host,dni,user,pas)

quots=SHD.get_options()
quots.change=quots.change/100


quotsCleaned = quots[quots["underlying_asset"].isin(['GGAL','YPFD','COME'])]
df2=quotsCleaned
df2=df2.drop(["bid_size", "bid", "ask", "ask_size",'expiration','strike','kind','underlying_asset'],axis=1)
df2["datetime"]= today
df2=df2.set_index("symbol")
data2= np.array(quotsCleaned["symbol"])

#quotsCleaned["datetime"] = quotsCleaned["datetime"].str.replace("Nan", "0")
#quotsCleaned["datetime"].replace("NaN","2015-01-01", inplace=True)

last_quot=wks.get_value((3,22))
if last_quot==stoday:
    for i in range(len(data2)):
        try:
            print(data2[i])
            result=pd.DataFrame(df2.loc[[data2[i]], :])
            result.to_sql(data2[i], index=False, con = engine, if_exists = 'append', chunksize = 1000)
        except:
            print(data2[i])
            result=pd.DataFrame(df2.loc[[data2[i]], :])
            result.to_sql(data2[i], index=False, con = engine, if_exists = 'replace', chunksize = 1000)
            print("New Created")

