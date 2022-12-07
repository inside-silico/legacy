from sqlalchemy import create_engine
import pandas as pd
import pymysql
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import date
import time

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="",
                               pw="",
                               db=""))


res = requests.get('https://ws.bolsar.info/BYMA/view/MontosNegociados.html')
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find_all('table')
data = pd.read_html(str(table))[0]
data.at[15,"Rubro"]="Préstamos Tit. Valores"
print(data)
#data.to_sql("Bolsar", con = engine, if_exists = 'replace', chunksize = 1000, index = False)


