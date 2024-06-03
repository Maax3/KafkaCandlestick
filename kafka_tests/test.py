import requests
import time
from datetime import datetime

def get_data():
  url = "https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers)
  return response.json()

while True:
  data = get_data()
  for moneda in data:
    tiempo = datetime.now()
    tiempo_actual_ms =  int(tiempo.timestamp() * 1000)
    print(f'Hora actual {tiempo_actual_ms}')
    print(f'La moneda es: {moneda[0]}')
    print(f'Los datos completos son: {moneda}')
  time.sleep(35)
