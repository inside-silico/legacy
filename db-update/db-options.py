import pandas as pd
import datetime
from datetime import date
import pygsheets
from oauth2client.service_account import  ServiceAccountCredentials
import time
import numpy as np

today = date.today()
stoday = today.strftime("%Y-%m-%d")

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')
sheetOut=gc.open("DB_Opciones")

sh = gc.open('Opciones')
wks = sh.worksheet_by_title("Cotizaciones")
quots = pd.DataFrame(wks.get_values('A2','s610'))

quots.columns=["symbol", "bid_size", "bid", "ask", "ask_size", "last","change", "open", "high", "low", "previous_close", "turnover", "volume",'operations', 'datetime','expiration','strike','kind','underlying_asset']
quotsCleaned = quots[quots["underlying_asset"].isin(['GGAL','YPFD','COME'])]
df2=quotsCleaned
df2=df2.drop(["bid_size", "bid", "ask", "ask_size",'expiration','strike','kind','underlying_asset'],axis=1)
df2["datetime"]= today
#df2["datetime"]="2021-08-26"
df2=df2.set_index("symbol")
data2= np.array(quotsCleaned["symbol"])
#quotsCleaned["datetime"] = quotsCleaned["datetime"].str.replace("Nan", "0")
#quotsCleaned["datetime"].replace("NaN","2015-01-01", inplace=True)
last_quot=wks.get_value((3,22))
if last_quot==stoday:
    for i in range(len(data2)):
        try:
            print(data2[i])
            wks = sheetOut.worksheet_by_title(data2[i])
            lenghtRow= wks.get_value((1,12))
            lenghtRow=int(lenghtRow) + 1
            result=pd.DataFrame(df2.loc[[data2[i]], :])
            wks.set_dataframe(result,(lenghtRow,1), copy_head = False)
            time.sleep(1.7)
        except:
            sheetOut.add_worksheet(data2[i])
            wks = sheetOut.worksheet_by_title(data2[i])
            wks.update_value('L1','=ArrayFormula(max(if(len(B:B),row(B:B),)))')
            result=pd.DataFrame(df2.loc[[data2[i]], :])
            wks.set_dataframe(result,(1,1), copy_head = True)
            print("New Created")
            time.sleep(2.7)

