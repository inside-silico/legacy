import requests
import json
import urllib3
urllib3.disable_warnings()
import pandas as pd
from pytz import timezone
from datetime import datetime
import datetime

s="S"
diction="s"
headers="s"

class openBYMAdata:
    def connect():
        global s
        global diction
        global headers
        s = requests.session()
        s.get('https://open.bymadata.com.ar/#/dashboard', verify=False)

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
        response = s.get('https://open.bymadata.com.ar/assets/api/langs/es.json', headers=headers)
        diction=json.loads(response.text)

    def marketTime():
        data = '{}'
        response = s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/market-time', headers=headers, data=data)
        return json.loads(response.text)

    def indices():
        data = '{"Content-Type":"application/json"}'
        response = s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/index-price', headers=headers, data=data, verify=False)
        indices = json.loads(response.text)['data']
        return pd.DataFrame(indices)

    def get_bonos():
        data = '{"page_number":1, "page_size":500, "Content-Type":"application/json"}'
        response = s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/bnown/seriesHistoricas/iamc/bonos', headers=headers, data=data)
        bonos_iamc = json.loads(response.text)
        return pd.DataFrame(bonos_iamc['data']).drop(["isin","notas"],axis=1)

    def get_lider():
        data = '{"excludeZeroPxAndQty":false,"T2":true,"T1":false,"T0":false,"Content-Type":"application/json"}' ## excluir especies sin precio y cantidad, determina plazo de listado
        response = s.post('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/leading-equity', headers=headers, data=data)
        panel_acciones_lideres = json.loads(response.text)
        return  pd.DataFrame(panel_acciones_lideres['data']).drop(["market","securityType","tickDirection","securityDesc","securitySubType","closingPrice","denominationCcy"],axis=1)



    def historicos(symbol,resolution,start_date,end_date):
        newyork_tz = timezone('America/Buenos_Aires')
        var = start_date.split("-")
        var = list(map(int, var))
        p1 = str(int(newyork_tz.localize(datetime.datetime(var[0],var[1],var[2], 8, 0, 0)).timestamp()))

        var = end_date.split("-")
        var = list(map(int, var))
        p2 = str(int(newyork_tz.localize(datetime.datetime(var[0],var[1],var[2], 8, 0, 0)).timestamp()))

        params = (
        ('symbol', symbol+' 48hs'),  ## Nombre de especie y plazo. 
        ('resolution', resolution), ## puede ser D - Diario, S - Semanal, M - Mensual, 
        ('from', str(p1)), ## Unix epoch, se deberia poder armar como int(datetime.datetime(AÑO,MES,DIA,HORA,MINUTOS).timestamp())
        ('to', str(p2)),
        )
        response = s.get('https://open.bymadata.com.ar/vanoms-be-core/rest/api/bymadata/free/chart/historical-series/history', params=params)
        df_historico = pd.DataFrame(json.loads(response.text))  # lo convierto en df
        df_historico['t'] = pd.to_datetime(df_historico['t'], unit='s').dt.normalize() # cambio el formato de la fecha. 
        df_historico.rename({'s':'status', 't':'date', 'c':'close', 'o':'open', 'h':'high', 'l':'low', 'v':'volume'}, axis = 1, inplace=True)
        return df_historico.drop(["status"],axis=1)

openBYMAdata.connect()
#print(openBYMAdata.marketTime())
#print(openBYMAdata.indices())
print(openBYMAdata.historicos("VSC1D","D","2016-11-16","2021-12-13"))
#print(openBYMAdata.get_bonos())
#print(openBYMAdata.get_lider())