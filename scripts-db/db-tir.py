from datetime import date
import requests
import urllib3
urllib3.disable_warnings()
import json
import pandas as pd
import numpy as np
import pygsheets

url = 'https://www.byma.com.ar/wp-admin/admin-ajax.php?action=get_bonos'
 
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
gc = pygsheets.authorize(service_file='')
sheetOut=gc.open("TIR_IAMC")

s = requests.session()
s.get('https://open.bymadata.com.ar/#/dashboard', verify=False)

## Fuerzo los headers que necesito (no se si es indispensable, pero asi me funciono)
headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://open.bymadata.com.ar',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://open.bymadata.com.ar/',
    'Accept-Language': 'es-US,es-419;q=0.9,es;q=0.8,en;q=0.7',
}

data = '{"page_number":1, "page_size":500, "Content-Type":"application/json"}'
response = s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/seriesHistoricas/iamc/bonos', headers=headers, data=data)
bonos_iamc = json.loads(response.text)
df = pd.DataFrame(bonos_iamc['data'])
df.set_index("symbol",inplace=True)

ticker=['AL29', 'AL29D', 'AL30','AL30D','AL35','AL35D','AE38','AE38D','AL41','AL41D','GD29','GD29D','GD30',	'GD30D','GD35',	'GD35D','GD38',	'GD38D','GD41',	'GD41D','GD46',	'GD46D']
last_TIR = pd.DataFrame(columns=[ticker])
df.rename(columns={"tirAnual":"TIR_Anual","paridad":"Paridad"},inplace=True)

print(df)

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
