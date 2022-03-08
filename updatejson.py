import requests
import json
import time
import os
import datetime
e = datetime.datetime.now()
while True:
  try:
    api = requests.get("http://data.fixer.io/api/latest?access_key=").json()
    print("Successfully got API on " + e.strftime("%Y-%m-%d %H:%M:%S"))
    with open("rate.json", "w") as r:
      r.write(json.dumps(api))
  except:
    print("Failed to get API")
  time.sleep(100000)
  