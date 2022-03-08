import json
import requests
import os
from pycoingecko import CoinGeckoAPI
from flask import Flask, request
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
            'amount':get_amount,
            'price':avnamt,
            'rate':get_rate
        }
    except:
        return {"error": "failed to get rate"}
@app.route("/api")
def index():
    return "<body><style> .footer { position: fixed; left: 10px; bottom: 5px; right: 10px; width: 95%; background-color: gray; color: white; text-align: center; } </style><h1>Endpoints:</h1><br><h2>/get?amount=(amount)&rate=(currency, currently you can only do all caps) | Get the price of avian in the currency of your choice. </h2></body><div class='footer'>Created by ayonull from the Avian Team - API Provided by CoinGecko and Fixer.io</div>"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    