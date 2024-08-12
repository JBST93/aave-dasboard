import requests

endpoint = "https://api.curve.fi/v1/getPools/big/ethereum"

r = requests.get(endpoint)
data = r.json()

pool = data.data.pooldata[0]
