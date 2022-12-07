import datetime
from pyhomebroker import HomeBroker
from sqlalchemy import create_engine
import pygsheets
import pandas as pd
from oauth2client.service_account import  ServiceAccountCredentials

engine = create_engine("mysql+pymysql://{user}:{pw}@flame2/{db}"
                       .format(user="",
                               pw="",
                               db=""))

broker = 
dni = ''
user = ''
password = ''

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='./client_secret.json')

hb = HomeBroker(int(broker))
hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)
#Conexion a Google Console
sh = gc.open('Bonos_DB')
wks = sh.worksheet_by_title("Bonos_AUX")
hb = HomeBroker(int(broker))
hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)

tickers = pd.DataFrame(wks.get_values('A2','A310'))



for i in range(len(tickers)):
        try:
                df= hb.history.get_intraday_history(tickers.at[i,0])
                try:
                        df=df.assign(F =0.1)
                        df.to_sql(tickers.at[i,0], con = engine, if_exists = 'append', chunksize = 1000)
                except:
                        df=df.assign(F =0.1)
                        df.to_sql(tickers.at[i,0], con = engine, if_exists = 'replace', chunksize = 1000)
        except:
                print("NoInfo at "+tickers.at[i,0])




