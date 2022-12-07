import dash
import dash_table
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import datetime
import numpy as np
from pandas.io.formats import style


from SHD import *




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server


host = ""  
dni = ""
usr = ""
pas = ""

SHD.catcher_connect(host,dni,usr,pas)
opex=datetime.datetime(2022, 6, 16)


def collar():
    source=SHD.get_options().set_index("symbol")
    last_GGAL=SHD.get_bluchips("48hs").set_index("symbol")
    last_GGAL=last_GGAL.at["GGAL","last"]

    time_left=((opex-datetime.datetime.now()))

    list_ticker=["GFGC84.0JU","GFGC87.0JU","GFGC90.0JU","GFGC93.0JU","GFGC96.0JU","GFGC99.0JU","GFGC102.JU","GFGC105.JU","GFGC108.JU","GFGC111.JU","GFGC114.JU","GFGC117.JU","GFGC120.JU","GFGC123.JU","GFGC126.JU","GFGC129.JU","GFGC132.JU","GFGC135.JU","GFGC140.JU","GFGC145.JU","GFGC150.JU","GFGC155.JU","GFGC160.JU","GFGC165.JU","GFGC170.JU","GFGC175.JU","GFGC180.JU","GFGC185.JU","GFGC190.JU","GFGC195.JU","GFGC200.JU","GFGC210.JU","GFGC220.JU","GFGC230.JU","GFGC240.JU","GFGC250.JU","GFGC260.JU","GFGC270.JU","GFGC280.JU","GFGC290.JU","GFGC300.JU","GFGC310.JU","GFGC320.JU","GFGC330.JU","GFGV84.0JU","GFGV87.0JU","GFGV90.0JU","GFGV93.0JU","GFGV96.0JU","GFGV99.0JU","GFGV102.JU","GFGV105.JU","GFGV108.JU","GFGV111.JU","GFGV114.JU","GFGV117.JU","GFGV120.JU","GFGV123.JU","GFGV126.JU","GFGV129.JU","GFGV132.JU","GFGV135.JU","GFGV140.JU","GFGV145.JU","GFGV150.JU","GFGV155.JU","GFGV160.JU","GFGV165.JU","GFGV170.JU","GFGV175.JU","GFGV180.JU","GFGV185.JU","GFGV190.JU","GFGV195.JU","GFGV200.JU","GFGV210.JU","GFGV220.JU","GFGV230.JU","GFGV240.JU","GFGV250.JU","GFGV260.JU","GFGV270.JU","GFGV280.JU","GFGV290.JU","GFGV300.JU","GFGV310.JU","GFGV320.JU","GFGV330.JU"]

    df=pd.DataFrame(columns=['symbol',"bid",'ask',"strike"])
    df.symbol=list_ticker
    df.set_index("symbol",inplace=True)

    df.update(source)
    pd_call=df.head(44).reset_index()
    pd_call.rename({"symbol":"symbolCall","bid":"bidCall","ask":"askCall"},axis=1,inplace=True)

    pd_put=df.tail(44).drop(["strike"],axis=1).reset_index()
    pd_put.rename({"symbol":"symbolPut","bid":"bidPut","ask":"askPut"},axis=1,inplace=True)

    result = pd.concat([pd_call, pd_put], axis=1, join="inner")
    result=result.reset_index().drop(["index"],axis=1)

    result=result.assign(Gain=0.0)
    result.Gain=(-last_GGAL+result.strike+result.bidCall-result.askPut)*100
    result.Gain=result.Gain.astype(float).round(2)
    result=result.assign(Gain2=0.0)
    result.Gain2=((result.Gain/100)/last_GGAL)*100
    result.Gain2=result.Gain2.astype(float).round(2)
    
    result.dropna(subset=['Gain'],inplace=True)
    
    result=result.assign(DaysLeft=0.0)
    result.DaysLeft=time_left.days+1
    result=result.assign(GainAnualized=0.0)
    result.GainAnualized=(result.Gain2/(time_left.days+1))*365

    result.rename({"Gain2":"GainPerc"},axis=1,inplace=True)

    df=result
    df=df.round(2)
    page= dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'filter_query': '{GainAnualized} > 33',
                    'column_id': c},
                    'backgroundColor': 'yellow',
                'color': 'black'
            } for c in df.columns
        ],
        style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white'
        },
        sort_action="native",
        sort_mode="single",)
    return page

def lanzamiento():
    df=SHD.get_options()
    last_GGAL=SHD.get_bluchips("48hs").set_index("symbol")
    last_underly=last_GGAL.at["GGAL","last"]

    df2=df[df["underlying_asset"].isin(["GGAL"])]
    #Descomentar para calcular solo vencimiento Abril 
    #df2=df2[df2["expiration"].isin([datetime.datetime(2022, 4, 13)])]
    df2=df2[df2["kind"].isin(["CALL"])]
    df2=df2[["symbol","strike","bid","ask","expiration"]].copy()
    df2=df2.assign(eq=0.0)
    df2=df2.assign(Clas=0.0)
    df2=df2.assign(gain=0.0)
    df2=df2.assign(gain2=0.0)
    df2=df2.assign(gain3=0.0)
    df2=df2.assign(days_left=0.0)
    df2.bid=df2.bid.astype(float)
    df2['eq'] = (last_underly-df2['bid'])
    df2.rename(columns={"eq": "Precio de Equilibrio"},inplace=True)
    def moneyness(x):
        if x <last_underly:
            return 'ITM'
        elif x > last_underly:
            return 'OTM'
        else:
            return 'ATM'
    df2['Clas'] = df2['strike'].apply(moneyness)
    df2.gain=(df2.bid+df2.strike-last_underly)*100
    df2.gain2=df2.gain/last_underly
    df2.days_left=(df2.expiration-datetime.datetime.now()).dt.days+1
    df2.gain3=(df2.gain2/df2.days_left)*365
    df2.rename(columns={"gain2": "Ganancia Potencial en %"},inplace=True)
    df2.rename(columns={"gain": "Ganancia Potencial"},inplace=True)
    df2.rename(columns={"gain3": "Ganancia Potencial en % Anualizada"},inplace=True)
    df2.rename(columns={"days_left": "Dias Restantes","symbol":"Ticker"},inplace=True)
    df2.drop(["expiration"],axis=1,inplace=True)
    df2=df2.set_index("Ticker")
    df2=df2.round(2)
    df2=df2.round(2)
    df2.reset_index(inplace=True)

    page= dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records'),
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'filter_query': '{GainPerc} > 4',
                    'column_id': c},
                    'backgroundColor': 'yellow',
                'color': 'black'
            } for c in df.columns
        ],
        style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white'
        },
        sort_action="native",
        sort_mode="single",)

    return page

def butterfly():
    source=SHD.get_options()

    list_ticker=["GFGC84.0JU","GFGC87.0JU","GFGC90.0JU","GFGC93.0JU","GFGC96.0JU","GFGC99.0JU","GFGC102.JU","GFGC105.JU","GFGC108.JU","GFGC111.JU","GFGC114.JU","GFGC117.JU","GFGC120.JU","GFGC123.JU","GFGC126.JU","GFGC129.JU","GFGC132.JU","GFGC135.JU","GFGC140.JU","GFGC145.JU","GFGC150.JU","GFGC155.JU","GFGC160.JU","GFGC165.JU","GFGC170.JU","GFGC175.JU","GFGC180.JU","GFGC185.JU","GFGC190.JU","GFGC195.JU","GFGC200.JU","GFGC210.JU","GFGC220.JU","GFGC230.JU","GFGC240.JU","GFGC250.JU","GFGC260.JU","GFGC270.JU","GFGC280.JU","GFGC290.JU","GFGC300.JU","GFGC310.JU","GFGC320.JU","GFGC330.JU"]
    list_strike=[84,87,90,93,96,99,102,105,108,111,114,117]
    data=pd.DataFrame(columns=['symbol',"bid",'ask',"strike"])
    data.symbol=list_ticker
    data.set_index("symbol",inplace=True)
    data.update(source.set_index("symbol"))
    data=data.assign(Clas=0.0)
    data=data.assign(Costo=0.0)
    data=data.assign(Ratio=0.0)
    data=data.assign(GanPot=0.0)
    data=data.assign(RunINF=0.0)
    data=data.assign(RunSUP=0.0)
    last_underly=210
    def moneyness(x):
        if x <last_underly:
            return 'ITM'
        elif x > last_underly:
            return 'OTM'
        else:
            return 'ATM'
    data['Clas'] = data['strike'].apply(moneyness)
    data.reset_index(inplace=True)
    for i in range(1,len(data)-1):
        data.at[i,"Costo"] = ((data.at[(i-1),"ask"])+(data.at[(i+1),"ask"])-(data.at[i,"bid"]*2))*100
        if (data.at[i,"strike"]==200):
            data.at[i,"Costo"] = ((data.at[(i-2),"ask"])+(data.at[(i+1),"ask"])-(data.at[i,"bid"]*2))*100

    for i in range(1,len(data)-1):
        data.at[i,"RunINF"] = (data.at[(i-1),"strike"])+(data.at[i,"Costo"]/100)
        if (data.at[i,"strike"]==200):
            data.at[i,"RunINF"] = (data.at[(i-2),"strike"])+(data.at[i,"Costo"]/100)
    
    for i in range(1,len(data)-1):
        data.at[i,"RunSUP"] = (data.at[(i+1),"strike"])-(data.at[i,"Costo"]/100)

    for i in range(1,len(data)-1):
        data.at[i,"GanPot"] = (((data.at[(i),"strike"])-(data.at[(i-1),"strike"]))*100)-data.at[(i),"Costo"]
        if (data.at[i,"strike"]==200):
            data.at[i,"GanPot"] = (((data.at[(i),"strike"])-(data.at[(i-2),"strike"]))*100)-data.at[(i),"Costo"]

    for i in range(1,len(data)-1):
        data.at[i,"Ratio"] = data.at[i,"GanPot"]/data.at[i,"Costo"]

    data.dropna(subset=['strike'],inplace=True)

    data=data.round(2)
    page= dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'filter_query': '{Costo} <-1',
                    'column_id': c},
                    'backgroundColor': 'yellow',
                'color': 'black'
            } for c in data.columns
        ],
        style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white'
        },
        sort_action="native",
        sort_mode="single",)

    return page


def bullspread():
    df=SHD.get_options()
    last_GGAL=SHD.get_bluchips("48hs").set_index("symbol")
    last_underly=last_GGAL.at["GGAL","last"]

    df2=df[df["underlying_asset"].isin(["GGAL"])]
    #Descomentar para calcular solo vencimiento Abril 
    df2=df2[df2["expiration"].isin([opex])]
    df2=df2[df2["kind"].isin(["CALL"])]
    df2=df2[["symbol","strike","bid","ask"]].copy()
    df2=df2.assign(Clas=0.0)
    df2=df2.assign(Costo=0.0)
    df2=df2.assign(Ratio=0.0)
    df2=df2.assign(GanPot=0.0)
    df2=df2.assign(GanPot2=0.0)
    def moneyness(x):
        if x <last_underly:
            return 'ITM'
        elif x > last_underly:
            return 'OTM'
        else:
            return 'ATM'
    df2['Clas'] = df2['strike'].apply(moneyness)
    df2.reset_index(inplace=True)
    for i in range(1,len(df2)):
        df2.loc[i,'Costo'] = (df2.at[(i-1),"ask"]-df2.at[(i),"bid"])*100

    for i in range(1,len(df2)):
        df2.loc[i,'GanPot'] = (df2.at[(i),"strike"]-df2.at[(i-1),"strike"]-(df2.at[i,"Costo"]/100))*100


    df2.GanPot2=df2.GanPot/df2.Costo
    df2.Ratio=df2.GanPot/df2.Costo
    df2=df2.round(2)
    df2.rename(columns={"GanPot2": "GanPot%"},inplace=True)
    df2.drop(["index"],axis=1,inplace=True)

    page= dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df2.columns],
        data=df2.to_dict('records'),
        style_cell_conditional=[    # align text columns to left. By default they are aligned to right
            {
                'if': {'filter_query': '{Ratio} > 1.99',
                    'column_id': c},
                    'backgroundColor': 'yellow',
                'color': 'black'
            } for c in df2.columns
        ],
        style_header={
        'backgroundColor': 'black',
        'fontWeight': 'bold',
        'color':'white'
        },
        sort_action="native",
        sort_mode="single",)

    return page


    
collar_layout =  html.Div([
    html.Div(id="collar-table"),
    dcc.Interval(
        id = 'collar-table-update',
        interval = 15000,
        n_intervals = 0
    ),])

lanzamiento_layout =  html.Div([
    html.Div(id="lanz-table"),
    dcc.Interval(
        id = 'lanz-table-update',
        interval = 15000,
        n_intervals = 0
    ),])

butterfly_layout =  html.Div([
    html.Div(id="butterfly-table"),
    dcc.Interval(
        id = 'butterfly-table-update',
        interval = 15000,
        n_intervals = 0
    ),])

bullspread_layout =  html.Div([
    html.Div(id="bullspread-table"),
    dcc.Interval(
        id = 'bullspread-table-update',
        interval = 15000,
        n_intervals = 0
    ),])


@app.callback(dash.dependencies.Output("collar-table", "children"), [ dash.dependencies.Input('collar-table-update', 'n_intervals') ])
def message(message):
    return collar()

@app.callback(dash.dependencies.Output("lanz-table", "children"), [ dash.dependencies.Input('lanz-table-update', 'n_intervals') ])
def message(message):
    return lanzamiento()

@app.callback(dash.dependencies.Output("butterfly-table", "children"), [ dash.dependencies.Input('butterfly-table-update', 'n_intervals') ])
def message(message):
    return butterfly()

@app.callback(dash.dependencies.Output("bullspread-table", "children"), [ dash.dependencies.Input('bullspread-table-update', 'n_intervals') ])
def message(message):
    return bullspread()

index_layout = html.Div( [ html.H3('Escribi bien salame')   ])
app.layout = html.Div(dcc.Location(id="url", refresh=True),id="page-content")

@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],)
def display_page(pathname="/"):
    ctx = dash.callback_context
    triggered_by = ctx.triggered[0].get("prop_id")

    if pathname == "/collar":
        return collar_layout

    elif pathname == "/lanzamiento":
        return lanzamiento_layout

    elif pathname == "/butterfly":
        return butterfly_layout

    elif pathname == "/bullspread":
        return bullspread_layout
    
    else:
        return index_layout


if __name__ == '__main__':
    app.run_server(debug=False,host='0.0.0.0')
