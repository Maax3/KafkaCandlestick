#::::::::::: DOCUMENTACION DE LA LIBRERIA ::::::::::::
# https://kafka-python.readthedocs.io/en/master/index.html
# https://fastavro.readthedocs.io/en/latest/writer.html

from kafka import KafkaProducer
import requests
import os
import time
from datetime import datetime
from io import BytesIO
from fastavro import writer
from fastavro.schema import load_schema

#Obtenemos el esquema AVRO del servicio registry-schema
SCHEMA_REGISTRY_URL = "http://localhost:8081/subjects/criptomonedas/versions/latest"
def fetch_schema(schema_registry_url):
    response = requests.get(schema_registry_url)
    schema_json = response.json()
    return schema_json['schema']

parsed_schema = fetch_schema(SCHEMA_REGISTRY_URL)

#Guardamos el esquema AVRO en un fichero.avsc
with open("esquema_avro.avsc", "w") as file:
    print('Fichero del esquema creado!')
    file.write(parsed_schema)

schema_path = os.path.join(os.path.dirname(__file__), 'esquema_avro.avsc')
schema = load_schema(schema_path)

# El metodo compara el esquema con el mensaje entrante, despues lo escribe en el stream y lo devuelve en bytes
def avro_serializer(mensaje):
    buffer = BytesIO()
    writer(buffer, schema, mensaje)
    buffer.seek(0)
    return buffer.read()



# Sacamos datos de la API publica
def get_data():
  url = "https://api-pub.bitfinex.com/v2/tickers?symbols=tBTCUSD,tETHUSD"
  headers = {"accept": "application/json"}
  response = requests.get(url, headers=headers)
  return response.json()

productor_bitfinex = KafkaProducer(
  bootstrap_servers= ['localhost:19092','localhost:19091','localhost:19090'],
  value_serializer=avro_serializer,
  acks='all'
)

# Mandamos los datos a Kafka
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
      #El productor distribuye cada moneda en particiones distintas segun su 'key' aka nombre
      productor_bitfinex.send(
      topic="criptomonedas",
      key=moneda_nombre.encode('utf-8'),
      timestamp_ms=tiempo_actual_ms,
      value= [{
          "nombre": moneda[0],
          "bid": float(moneda[1]),
          "bid_size": float(moneda[2]),
          "ask": float(moneda[3]),
          "ask_size": float(moneda[4]),
          "daily_change": float(moneda[5]),
          "daily_change_percentage": float(moneda[6]),
          "precio_ultimo": float(moneda[7]),
          "volume": float(moneda[8]),
          "precio_maximo": float(moneda[9]),
          "precio_minimo": float(moneda[10])
      }]
    )
    print('Petición realizada!')
    time.sleep(15)