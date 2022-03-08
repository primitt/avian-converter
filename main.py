import json
import requests
import os
from pycoingecko import CoinGeckoAPI
from flask import Flask
app = Flask(__name__)

from flask import request

@app.route('/data')
def data(user):
  user = request.args.get('user')
  return user
#import updatejson
#get the API
# rates_api = requests.get("http://data.fixer.io/api/latest?access_key=ac697ae49feb83aee98629941b57a547").json()
#get secondary API
with open('rate.json') as f:
   rates_api = json.load(f)
# Coin Gecko API
cg = CoinGeckoAPI()
get_avianUSD = cg.get_price(ids="avian-network", vs_currencies="USD")
format_avianUSD = get_avianUSD['avian-network']['usd']
print("Price of avian", "$" + str(format_avianUSD))
while True:
  try:
    rate_get = input("Enter Wanted Rate: ")
    get_usd = rates_api["rates"][rate_get]
    break
  except:
    print("Failed to get price! Please try again")
    print(get_usd)
amt_get = format_avianUSD
timevalue = float(get_usd)*float(amt_get)
print(timevalue, rate_get, "is " + str(amt_get) +" USD")
get_amountAVN = input("Enter amount of AVN: ")
amtAVN_price = float(get_amountAVN)*float(timevalue)
print(get_amountAVN, "is worth", amtAVN_price, rate_get)
dictavn = {
  'amount':get_amountAVN,
  'price':amtAVN_price,
  'rate':rate_get
}
print(dictavn)
with open("api.json", "w") as f:
  f.write(json.dumps(dictavn))
  print("Sucessfully wrote API to file")
