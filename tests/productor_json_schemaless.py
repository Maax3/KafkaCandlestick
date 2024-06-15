#::::::::::: DOCUMENTACION DE LA LIBRERIA ::::::::::::
# https://kafka-python.readthedocs.io/en/master/index.html

from kafka import KafkaProducer
import requests
import json
import time
from datetime import datetime


# Sacamos datos de la API publica
def get_data():
  url = "https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers)
  return response.json()

def serializer(mensaje):
  return json.dumps(mensaje).encode('utf-8')

productor_bitfinex = KafkaProducer(
  bootstrap_servers= ['localhost:19092','localhost:19091','localhost:19090'],
  value_serializer=serializer,
  acks='all'
)

if __name__ == '__main__':
  while True:
    try: 
      data = get_data()
    except Exception as error:
      print(error)
      time.sleep(60)
      continue

    for moneda in data:
      moneda_nombre = moneda[0]
      tiempo = datetime.now()
      tiempo_actual_ms =  int(tiempo.timestamp() * 1000)
      #El productor distribuye cada moneda en particiones distintas segun su 'key' aka nombr
      productor_bitfinex.send(
      topic="criptomonedas",
      key=moneda_nombre.encode('utf-8'),
      value=moneda,
      timestamp_ms=tiempo_actual_ms
    )
    time.sleep(15)