import json
import requests
import os
from pycoingecko import CoinGeckoAPI
from flask import Flask, request, render_template
app = Flask(__name__)
with open('rate.json') as f:
   rates_api = json.load(f)
# Coin Gecko API
cg = CoinGeckoAPI()
get_avianUSD = cg.get_price(ids="avian-network", vs_currencies="EUR")
format_avianUSD = get_avianUSD['avian-network']['eur']

@app.route('/get', methods=['GET'])
def search():
    args = request.args
    try:
        get_amount = args.get("amount")
        get_rate = args.get("rate")
        try:
            get_usd = rates_api["rates"][get_rate]
        except:
            return {"error":"invalid rate"}
        try:
            timevalue = float(get_usd)*float(format_avianUSD)
            avnamt = float(get_amount)*float(timevalue)
        except:
            return {"error":"invalid amount"}
        return {
            "amount":get_amount,
            "price":avnamt,
            "rate":get_rate
        }
    except:
        return {"error": "failed to get rate"}
    # try:
    #   get_full = args.get("full")
    #   try:
    #     full = bool(get_full)
    #     if full == True:
    #       return rates_api
    #   except:
    #     return {"error":"Not a bool"}
    # except:
    #   pass
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/get/<name>")
def error(name):
  return {"error":"not an endpoint"}
@app.route("/get/full")
def full():
  return rates_api
@app.route("/<name>")
def error():
  return {"error":"not an endpoint"}
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    