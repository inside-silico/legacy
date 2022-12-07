import pandas as pd

from datetime import date, datetime
import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import time
import numpy as np
from sqlalchemy import create_engine

nan_value = float("NaN")
today = date.today()
stoday = today.strftime("%Y-%m-%d")


engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="",
                               pw="",
                               db=""))

engine2 = create_engine("mysql+pymysql://{user}:{pw}@{db_host}/{db}"
                       .format(db_host="sql10.freemysqlhosting.net",pw="",user="",
                               db="",))


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')

sh = gc.open('WebApp_Sheet')
wks = sh.worksheet_by_title("Bonos_0.8.0")
quots = pd.DataFrame(wks.get_values('A1','J610'))
quots.columns=quots.loc[[0]].values.flatten().tolist()
quots=quots.drop(0)

df2=quots[["Ticker","Paridad","TIR"]].copy()
df2.TIR=df2.TIR.str.replace("%","")
df2.TIR=df2.TIR.str.replace("Sin Datos","0.0")
df2.TIR=df2.TIR.astype(float)/100
df2.Paridad=df2.Paridad.str.replace("Sin Datos","0.0")
df2.Paridad=df2.Paridad.astype(float)
df2=df2.assign(F = today)
df2=df2.rename(columns = {'F': 'date'})

df2=df2[["date","Ticker","Paridad","TIR"]]
df2=df2.rename(columns = {'Paridad': 'PAR'})


#df2["datetime"]="2021-11-12"

data2= np.array(df2["Ticker"])
df2=df2.set_index("Ticker")

last_quot=sh.worksheet_by_title("Panel").get_value(("S3"))
last_quot=stoday
if last_quot==stoday:
    for i in range(len(data2)):
        try:
            result=pd.DataFrame(df2.loc[[data2[i]], :])
            result.to_sql(data2[i], con = engine, if_exists='append', chunksize = 1000, index=False)
            result.to_sql(data2[i], con = engine2, if_exists='append', chunksize = 1000, index=False)
            print(result)
        except:
            print("Check")

