import json
import requests
import os
from pycoingecko import CoinGeckoAPI
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
with open('rate.json') as f:
   rates_api = json.load(f)
# Coin Gecko API
cg = CoinGeckoAPI()
get_avianUSD = cg.get_price(ids="avian-network", vs_currencies="EUR")
format_avianUSD = get_avianUSD['avian-network']['eur']

@app.route('/', methods=['GET'])
def search():
    args = request.args
    try:
        get_amount = args.get("amount")
        get_rate = args.get("rate")
        rate_formatted = get_rate.upper()
        try:
            get_usd = rates_api["rates"][rate_formatted]
        except:
            return redirect("./docs/api")
        try:
            timevalue = float(get_usd)*float(format_avianUSD)
            avnamt = float(get_amount)*float(timevalue)
        except:
            return redirect("./docs/api")
        return {
            "amount":get_amount,
            "price":avnamt,
            "rate":get_rate
        }
    except:
        return redirect("./docs/api")
@app.route("/docs/api")
def index():
    return render_template("index.html")
# @app.route("/<name>")
# def error(name):
#   return {"error":"not an endpoint"}
@app.route("/all")
def full():
  return rates_api
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    