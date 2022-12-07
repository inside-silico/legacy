import os
import plotly.graph_objs as go 
from sfft_v1 import *
from dash import html
import plotly.express as px
from dash import dcc
import pandas as pd
from layout import *
from layout_minimal import *
from pyhomebroker import HomeBroker
import datetime
from datetime import date


line1="#f4c100"
line2="#e6550d"
line3="#de2d26"

class graphics:
    def mep_graph(ticker):

        today = datetime.date.today()
        broker = 
        dni = ''
        user = ''
        password = ''
        hb = HomeBroker(int(broker))
        hb.auth.login(dni=dni, user=user, password=password, raise_exception=True)

        GD30_df=hb.history.get_daily_history(ticker, datetime.date(2005,1, 1), today)

        GD30_df=GD30_df[["date","close"]].copy()
        GD30_df.columns=["date","GD30"]

        ticker_d=ticker+"D"
        GD30D_df=hb.history.get_daily_history(ticker_d, datetime.date(2005,1, 1), today)
        GD30D_df=GD30D_df[["date","close"]].copy()
        GD30D_df.columns=["date","GD30D"]
        GD30D_df

        mep30=pd.DataFrame(columns=['date','GD30','GD30D','mepGD30'])

        mep30.date=GD30_df.date
        mep30=mep30.set_index("date")
        
        GD30_df=GD30_df.set_index("date")

        mep30.update(GD30_df)
        GD30D_df=GD30D_df.set_index("date")
        mep30.update(GD30D_df)
        mep30.mepGD30=mep30.GD30/mep30.GD30D
        mep30=mep30.reset_index()

        fig = go.Figure(layout=go.Layout(layout.layout_minimal()))

        fig.add_trace(go.Scatter(x= mep30.date, y=mep30.mepGD30,line=dict(color=line1)))
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False,type="log")
        fig.update_layout(title="MEP "+ticker, title_x=0.5)
        #fig.update_traces(line=dict(width=2,color='yellow'))
        fig.update_xaxes(rangeselector_bgcolor="black")
   
        return fig

    def dolar_ambito(value):
        title_selected="dd"
        df=pd.DataFrame()
        if value=="Dolar Oficial":
            df= ambito.dolar_oficial("2020-03-01",date.today().strftime("%Y-%m-%d"))
            title_selected="Dolar Oficial"
            bad_value=datetime.date(2021,8,18)
            df =df.query("Fecha != @bad_value")

        if value=="Dolar Blue":
            df= ambito.dolar_blue("2020-03-01",date.today().strftime("%Y-%m-%d"))
            title_selected="Dolar Blue"
        if value=="Dolar Solidario":
            df= ambito.dolar_solidario("2020-03-01",date.today().strftime("%Y-%m-%d"))
            bad_value=datetime.date(2021,8,18)
            df =df.query("Fecha != @bad_value")
            title_selected="Dolar Solidario"
        
        fig = go.Figure(layout=go.Layout(layout.layout_minimal()))
        fig.add_trace(go.Scatter(x= df.Fecha, y=df.Venta,line=dict(color=line1)))
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False,type="log")
        fig.update_layout(title=title_selected, title_x=0.5)
        #fig.update_traces(line=dict(width=2,color='yellow'))
        fig.update_xaxes(rangeselector_bgcolor="black")
        page =html.Div(children=[dcc.Graph(figure=fig)])
        return page

    def brecha():
        df1= ambito.dolar_oficial("2020-03-01",date.today().strftime("%Y-%m-%d"))
        df2= ambito.dolar_blue("2020-03-01",date.today().strftime("%Y-%m-%d"))
        df2.columns=["date","Compra","Blue"]
        df2.set_index("date")

        brecha=pd.DataFrame(columns=['date','Oficial','Blue','Brecha'])
        brecha.date=df1.Fecha.copy()
        brecha.set_index("date")
        brecha.Oficial=df1.Venta.copy()
        brecha.update(df2)
        brecha.Brecha=(brecha.Blue/brecha.Oficial)-1
        brecha.reset_index()

        fig = go.Figure(layout=go.Layout(layout.layout_minimal()))

        fig.add_trace(go.Scatter(x= brecha.date, y=brecha.Brecha,line=dict(color=line1)))
        fig.update_traces(connectgaps=True)
        fig.update_yaxes(fixedrange=False)
        fig.update_layout(title="Brecha Dolar Blue - Dolar Oficial ", title_x=0.5)
        #fig.update_traces(line=dict(width=2,color='yellow'))
        fig.update_xaxes(rangeselector_bgcolor="black")
   
        return fig
