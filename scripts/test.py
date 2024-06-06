import os
import threading
import fastavro
import json
import influxdb_client
import datetime as dt
from dotenv import load_dotenv
from kafka import KafkaConsumer
from io import BytesIO
from fastavro.schema import parse_schema
from productor_avro import fetch_schema
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

load_dotenv()

#::::ESTE ARCHIVO SIMULA 2 CONSUMIDORES MEDIANTE HILOS:::
schema = json.loads(fetch_schema(os.getenv("SCHEMA_URL"))) #convierte str a json
avro_schema = parse_schema(schema)


#::::CONFIGURACION DE LOS CONSUMIDORES:::
conf = {
  "bootstrap_servers": ['localhost:19092', 'localhost:19091', 'localhost:19090'],
  "auto_offset_reset": 'earliest',
  "enable_auto_commit": True,
  "group_id": 'Coins'
}

consumidor_1 = KafkaConsumer(
       "criptomonedas",
       client_id="Jamon",
       **conf,
)

consumidor_2 = KafkaConsumer(
       "criptomonedas",
       client_id="Bacon",
       **conf,
)


influxdb_client = InfluxDBClient(
  url=os.getenv("URL_SERVER"), 
  token=os.getenv("TOKEN"), 
  org=os.getenv("ORG")
)

bucket="criptodata"
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

# Función para deserializar mensajes Avro
def avro_decoder(message_value):
    bytes_reader = BytesIO(message_value)
    reader = fastavro.reader(bytes_reader, avro_schema)
    for mensaje in reader:
        return mensaje

# Función para consumir mensajes y escribir en InfluxDB
def ver_mensajes(consumer):
  for message in consumer:
    mensaje = avro_decoder(message.value)
    print(f"El {consumer.config['client_id']} se ha ocupado del: {mensaje}\n")
    
    #tiempo_actual = dt.datetime.now()
    #timestamp = int(tiempo_actual.timestamp())
    tiempo_actual = dt.datetime.utcnow()
    timestamp = tiempo_actual.isoformat() + 'Z'  # Añadir 'Z' para indicar que es en formato UTC
    registro = (
      Point("criptomonedas")
      .tag("Moneda", mensaje['nombre'])
      .field("Precio", mensaje['precio_ultimo'])).time(timestamp)
    
    write_api.write(bucket=bucket, org=os.getenv("ORG"), record=registro)

# Creamos un hilo para cada consumidor, o en otras palabras, asignamos la funcion ver_mensajes a cada consumidor
threads = []
consumer_group = [consumidor_1, consumidor_2]
for consumidor in consumer_group:
   hilo = threading.Thread(target=ver_mensajes, args=(consumidor,))
   hilo.start()
   threads.append(hilo)

for hilo in threads:
   hilo.join()
