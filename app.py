import json
import requests
import os
from pycoingecko import CoinGeckoAPI
from flask import Flask, request, render_template, redirect
app = Flask(__name__)
#fixer.io API
with open('rate.json') as f:
   rates_api = json.load(f)
# Coin Gecko API
cg = CoinGeckoAPI()
# Exbitron API
exbit_api = requests.get("https://www.exbitron.com/api/v2/peatio/public/markets/avnusdt/depth").json()
exbit_price = float(exbit_api["asks"][0][0])
# CoinGecko Integration
get_avianUSD = cg.get_price(ids="avian-network", vs_currencies="EUR")
format_avianUSD = float(get_avianUSD['avian-network']['eur'])
averaged = (exbit_price+format_avianUSD)/2
@app.route('/get', methods=['GET'])
def search():
    args = request.args
    try:
        get_amount = args.get("amount")
        get_rate = args.get("rate")
        rate_formatted = get_rate.upper()
        try:
            get_usd = rates_api["rates"][rate_formatted]
        except:
            return redirect("./api/docs/api")
        try:
            timevalue = float(get_usd)*float(averaged)
            avnamt = float(get_amount)*float(timevalue)
        except:
            return redirect("./api/docs/api")
        return {
            "amount":get_amount,
            "price":avnamt,
            "rate":get_rate
        }
    except:
        return redirect("./api/docs/api")
@app.route("/docs/api")
def index():
    return render_template("index.html")
@app.route("/get/<name>")
def error(name):
  return {"error":"not an endpoint"}
@app.route("/get/all")
def full():
  return rates_api
@app.route("/get/price")
def ex():
    return {"exbitron" : exbit_price, "coingecko":format_avianUSD, "averaged":averaged}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    