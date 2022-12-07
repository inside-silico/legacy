import flask
from SHD import *
import pandas as pd
from functions import *

from open_chori import *
chori=openBYMAdata()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

host = ""
dni = ""
usr = ""
pas = ""

SHD.catcher_connect(host,dni,usr,pas)

@app.route('/api/arg/bonds/48hs', methods=['GET'])
def bonds48hs():
    df=SHD.get_bonds("48hs").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")
    
@app.route('/api/arg/bonds/spot', methods=['GET'])
def bondsspot():
    df=SHD.get_bonds("spot").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")

@app.route('/api/arg/cedears/48hs', methods=['GET'])
def cedear48():
    df=SHD.get_cedear("48hs").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")

@app.route('/api/arg/cedears/48hs', methods=['GET'])
def cedearspot():
    df=SHD.get_cedear("spot").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")

@app.route('/api/arg/bluechips/48hs', methods=['GET'])
def bluechips():
    df=SHD.get_bluchips("48hs").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")

@app.route('/api/arg/galpones/48hs', methods=['GET'])
def galpons():
    df=SHD.get_galpones("48hs").drop(["group"],axis=1)
    print(df)
    return df.to_json(orient="records")

@app.route('/api/arg/options', methods=['GET'])
def options():
    df=SHD.get_options(orient="records")
    print(df)
    return df.to_json()
    
@app.route('/api/arg/indices', methods=['GET'])
def indecs():
    df=SHD.get_MERV().drop(["group"],axis=1)
    print(df)
    return df.to_json()

@app.route('/api/arg/cedear-ccl', methods=['GET'])
def cedear_ccl():
    return ccl().to_json(orient="records")

@app.route('/api/us/stocks', methods=['GET'])
def stocks():
    return outer_quots().to_json(orient="records")

@app.route('/api/arg/dashboard/bonds', methods=['GET'])
def bonds_dash():
    df=pd.read_csv(" ")
    return df.to_json(orient="records")

@app.route('/api/arg/mainVar', methods=['GET'])
def bcra_endpoint():
    return bcra().to_json(orient="records")

@app.route('/api/arg/BYMAnews', methods=['GET'])
def news_endpoint():
    return chori.byma_news().to_json(orient="records")


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=80)
