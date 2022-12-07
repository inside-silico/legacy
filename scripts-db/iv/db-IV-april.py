from functions import *
from sfft_v1 import *
import pandas as pd
import datetime
from SHD import *
from account import *
from sqlalchemy import create_engine

opex=datetime.datetime(2022, 4, 13)

SHD.catcher_connect(host,dni,usr,pas)

df=SHD.get_options()
df=df.assign(last_underly=0.0)
last_GGAL=SHD.get_bluchips("48hs").set_index("symbol")
last_date=last_GGAL.at["GGAL","datetime"]
last_GGAL=last_GGAL.at["GGAL","last"]
df.last_underly=last_GGAL

df2=df[df["underlying_asset"].isin(["GGAL"])]
df2=df2[df2["expiration"].isin([opex])]
df2=df2[df2["kind"].isin(["CALL"])]
df2=df2.assign(DIF=0.0)
df2.DIF=df2.last_underly-df2.strike
df2.DIF=df2.DIF.abs()

output=df2[df2["DIF"].isin([df2.DIF.min()])][["symbol","last","strike","expiration","last_underly"]].copy()
output.reset_index(inplace=True)
output=output.assign(IV=0.0)

output=output.assign(time_left=0.0)
time_left=((opex-datetime.datetime.now()))

output.time_left=time_left.days
output.IV=implied_volatility_call(output.at[0,"last_underly"],output.at[0,"strike"],float((time_left.days+1)/365),0.33,output.at[0,"last"])
output.drop(["index"],axis=1,inplace=True)

engine = create_engine("mysql+pymysql://{user}:{pw}@flame2/{db}"
                       .format(user="c",
                       .format(user="c",

                               pw="",
                               db=""))

output.to_sql("april", index=False, con = engine, if_exists = 'append', chunksize = 1000)
