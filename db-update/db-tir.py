from datetime import date
import requests
import json
import pandas as pd
import numpy as np
import pygsheets

url = 'https://www.byma.com.ar/wp-admin/admin-ajax.php?action=get_bonos'
 
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file=' ')
sheetOut=gc.open("TIR_IAMC")

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

page = requests.get(url, headers=headers, timeout=5)
data = page.json()
#df=pd.DataFrame(data["Cotizaciones"])
df=pd.DataFrame(data["IndicesBonos"])
df = df.set_index("Codigo")
#df = df.rename(columns = {'Simbolo': 'Ticker'}, inplace = False)
#df = df.set_index("Ticker")
pd.set_option('compute.use_numexpr', False)
ticker=['AL29', 'AL29D', 'AL30','AL30D','AL35','AL35D','AE38','AE38D','AL41','AL41D','GD29','GD29D','GD30',	'GD30D','GD35',	'GD35D','GD38',	'GD38D','GD41',	'GD41D','GD46',	'GD46D']
last_TIR = pd.DataFrame(columns=[ticker])
df['TIR_Anual']=df['TIR_Anual']/100
df['Paridad']=df['Paridad']/100

today = date.today()
stoday = today.strftime("%d-%m-%Y")
last_TIR.loc[0] = [df.at[ticker[0],'TIR_Anual'],df.at[ticker[1],'TIR_Anual'],df.at[ticker[2],'TIR_Anual'],df.at[ticker[3],'TIR_Anual'],df.at[ticker[4],'TIR_Anual'],df.at[ticker[5],'TIR_Anual'],df.at[ticker[6],'TIR_Anual'],df.at[ticker[7],'TIR_Anual'],df.at[ticker[8],'TIR_Anual'],df.at[ticker[9],'TIR_Anual'],df.at[ticker[10],'TIR_Anual'],df.at[ticker[11],'TIR_Anual'],df.at[ticker[12],'TIR_Anual'],df.at[ticker[13],'TIR_Anual'],df.at[ticker[14],'TIR_Anual'],df.at[ticker[15],'TIR_Anual'],df.at[ticker[16],'TIR_Anual'],df.at[ticker[17],'TIR_Anual'],df.at[ticker[18],'TIR_Anual'],df.at[ticker[19],'TIR_Anual'],df.at[ticker[20],'TIR_Anual'],df.at[ticker[21],'TIR_Anual']]
last_par = pd.DataFrame(columns=[ticker])
last_par.loc[0] = [df.at[ticker[0],'Paridad'],df.at[ticker[1],'Paridad'],df.at[ticker[2],'Paridad'],df.at[ticker[3],'Paridad'],df.at[ticker[4],'Paridad'],df.at[ticker[5],'Paridad'],df.at[ticker[6],'Paridad'],df.at[ticker[7],'Paridad'],df.at[ticker[8],'Paridad'],df.at[ticker[9],'Paridad'],df.at[ticker[10],'Paridad'],df.at[ticker[11],'Paridad'],df.at[ticker[12],'Paridad'],df.at[ticker[13],'Paridad'],df.at[ticker[14],'Paridad'],df.at[ticker[15],'Paridad'],df.at[ticker[16],'Paridad'],df.at[ticker[17],'Paridad'],df.at[ticker[18],'Paridad'],df.at[ticker[19],'Paridad'],df.at[ticker[20],'Paridad'],df.at[ticker[21],'Paridad']]
print(last_par)
print(last_TIR)

wks = sheetOut.worksheet_by_title("Paridad")
lenghtRow= wks.get_value((1,26))
lenghtRow=int(lenghtRow)
wks.set_dataframe(last_par,(lenghtRow,2), copy_head = False)
wks = sheetOut.worksheet_by_title("TIR")
wks.set_dataframe(last_TIR,(lenghtRow,2), copy_head = False)
