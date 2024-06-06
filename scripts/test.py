from kafka import KafkaConsumer
import threading
from io import BytesIO
import fastavro
from fastavro.schema import parse_schema
from productor_avro import fetch_schema
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision

#::::ESTE ARCHIVO SIMULA 2 CONSUMIDORES MEDIANTE HILOS:::

SCHEMA_URL = "http://localhost:8081/subjects/criptomonedas/versions/latest"
schema = json.loads(fetch_schema(SCHEMA_URL)) #convierte str a json
avro_schema = parse_schema(schema)

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

# Conexión a InfluxDB
influxdb_client = InfluxDBClient(url="http://localhost:8086", token="your_token", org="your_org")
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
bucket = "your_bucket"

# Función para deserializar mensajes Avro
def avro_decoder(message_value):
    bytes_reader = BytesIO(message_value)
    reader = fastavro.reader(bytes_reader, avro_schema)
    for mensaje in reader:
        return mensaje

# Función para consumir mensajes y escribir en InfluxDB
def ver_mensajes(consumer):
  for message in consumer:
    message_value = message.value
    avro_record = avro_decoder(message_value)
    print(f"El {consumer.config['client_id']} se ha ocupado del: {avro_record}\n")
    point = Point("criptomonedas").tag("client_id", consumer.config['client_id']).field("data", avro_record)
    write_api.write(bucket=bucket, record=point)

# Creamos un hilo para cada consumidor, o en otras palabras, asignamos la funcion ver_mensajes a cada consumidor
threads = []
consumer_group = [consumidor_1, consumidor_2]
for consumidor in consumer_group:
   hilo = threading.Thread(target=ver_mensajes, args=(consumidor,))
   hilo.start()
   threads.append(hilo)

for hilo in threads:
   hilo.join()
