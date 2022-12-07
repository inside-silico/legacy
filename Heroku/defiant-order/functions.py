import pandas as pd
from sfft_v1 import *
from SHD import *
from bs4 import BeautifulSoup

host = ""  
dni = ""
usr = ""
pas = ""


SHD.catcher_connect(host,dni,usr,pas)

def ccl():
    source=SHD.get_cedear("48hs")
    source.rename({"last":"Cedear","symbol":"Ticker"},axis=1,inplace=True)
    source.set_index("Ticker",inplace=True)

    list_ticker=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DISN","EBAY","ERJ","FB","GE","GLNT","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TEN","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
    list_outer=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DIS","EBAY","ERJ","FB","GE","GLOB","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TS","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
    yahoo_outer=  ','.join(map(str, list_outer))
    yahoo_outer='"'+yahoo_outer+'"'
    list_fc=[10.0,0.5,144.0,0.5,1.0,6.0,9.0,1.0,3.0,5.0,8.0,1.0,4.0,2.0,1.0,8.0,1.0,6.0,1.0,58.0,1.0,5.0,5.0,1.0,5.0,5.0,5.0,8.0,60.0,10.0,16.0,24.0,1.0,2.0,11.0,3.0,1.0,15.0,6.0,2.0,0.2,2.0,5.0,6.0,3.0]

    ccl_columns=["Ticker","TickerUS","FC","Cedear","Stock","CCL"]
    ccl=pd.DataFrame(columns=ccl_columns)
    ccl.Ticker=list_ticker
    ccl.TickerUS=list_outer
    ccl.FC=list_fc
    ccl.FC=ccl.FC.astype(float)

    outer_quots=yahoo.get_quotes(yahoo_outer)
    print(outer_quots)
    outer_quots.rename({"last":"Stock","symbol":"Ticker"},axis=1,inplace=True)
    ccl.set_index("TickerUS",inplace=True)
    ccl.update(outer_quots.set_index("Ticker"))
    ccl.reset_index(inplace=True)
    ccl.set_index("Ticker",inplace=True)
    ccl.update(source)
    ccl.reset_index(inplace=True)

    ccl.CCL=(ccl.Cedear/ccl.Stock)*ccl.FC

    return ccl

def outer_quots():
    list_outer=["AAPL","AMD","AMZN","ARCO","AUY","BA","BABA","BBD","C","CSCO","CVX","DESP","DIS","EBAY","ERJ","FB","GE","GLOB","GOLD","GOOGL","HMY","IBM","INTC","ITUB","JNJ","JPM","KO","MCD","MELI","MSFT","NFLX","NVDA","PBR","PFE","QCOM","T","TS","TSLA","V","VALE","VIST","VZ","WFC","WMT","X"]
    yahoo_outer=  ','.join(map(str, list_outer))
    yahoo_outer='"'+yahoo_outer+'"'
    outer_quots=yahoo.get_quotes(yahoo_outer)
    return outer_quots

def bcra():
    res = requests.get('http://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp')
    soup = BeautifulSoup(res.content, 'html.parser')
    table = soup.find_all('table')
    data = pd.read_html(str(table))[0]
    data.at[15,"Rubro"]="Préstamos Tit. Valores"
    data.dropna(subset=["Valor"],inplace=True)
    data.drop(["Rubro"],axis=1,inplace=True)
    data.set_index("Unnamed: 0",inplace=True)
    data.drop("Tasas de interés",inplace=True)
    data.reset_index(inplace=True)
    data.Valor=data.Valor.str.replace(".", "").astype(float)
    row10=[28,30,31,32,33]
    row100=[1,2,3,4,5,6,7,11,12,13,14,15,16,17,35,36]
    row10000=[8,9,10,34]

    for i in range(len(row10)):
        data.at[row10[i],"Valor"]=data.at[row10[i],"Valor"]/10

    for i in range(len(row100)):
        data.at[row100[i],"Valor"]=data.at[row100[i],"Valor"]/100

    data.at[0,"Valor"]=data.at[0,"Valor"]/1000

    for i in range(len(row10000)):
        data.at[row10000[i],"Valor"]=data.at[row10000[i],"Valor"]/10000

    return data

def ccl_adr():
    source=SHD.get_bluchips("48hs")
    source.rename({"last":"ADR","symbol":"Ticker"},axis=1,inplace=True)
    source.set_index("Ticker",inplace=True)

    source2=SHD.get_galpones("48hs")
    source2.rename({"last":"ADR","symbol":"Ticker"},axis=1,inplace=True)
    source2.set_index("Ticker",inplace=True)

    list_ticker=["GGAL","YPFD",		"PAMP",	"LOMA",	"BMA",	"CEPU",	"EDN",	"SUPV",	"BBAR",	"CRES",	"TECO2",	"TGSU2",	"IRSA",	"IRCP"]
    ticker_outer=["GGAL","YPF",		"PAM",	"LOMA",	"BMA",	"CEPU",	"EDN",	"SUPV",	"BBAR",	"CRESY",	"TEO",	"TGS",	"IRS",	"IRCP"]
    list_outer=["VOID","GGAL","YPF",		"PAM",	"LOMA",	"BMA",	"CEPU",	"EDN",	"SUPV",	"BBAR",	"CRESY",	"TEO",	"TGS",	"IRS",	"IRCP","VOID"]
    yahoo_outer=  ','.join(map(str, list_outer))
    yahoo_outer='"'+yahoo_outer+'"'
    list_fc=[10,1,	25,	5,	10,	10,	20,	5,	3,	10,	5,	5,	10,	4]

    ccl_columns=["Ticker","TickerUS","FC","ADR","Stock","CCL"]
    ccl=pd.DataFrame(columns=ccl_columns)
    ccl.Ticker=list_ticker
    ccl.TickerUS=ticker_outer
    ccl.FC=list_fc
    ccl.FC=ccl.FC.astype(float)

    outer_quots=yahoo.get_quotes(yahoo_outer)
    outer_quots.rename({"last":"Stock","symbol":"Ticker"},axis=1,inplace=True)
    ccl.set_index("TickerUS",inplace=True)
    ccl.update(outer_quots.set_index("Ticker"))
    ccl.reset_index(inplace=True)
    ccl.set_index("Ticker",inplace=True)
    ccl.update(source)
    ccl.update(source2)
    ccl.reset_index(inplace=True)

    ccl.CCL=(ccl.ADR/ccl.Stock)*ccl.FC
    return ccl
