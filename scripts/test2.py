from kafka import KafkaConsumer
import os
import time
from io import BytesIO
from fastavro import reader
from fastavro.schema import load_schema

SCHEMA_REGISTRY_URL = "http://localhost:8081/subjects/criptomonedas/versions/latest"
schema_path = os.path.join(os.path.dirname(__file__), 'esquema_avro.avsc')
schema = load_schema(schema_path)

def avro_decoder(mensaje):
    buffer = BytesIO(mensaje)
    reader = reader(buffer, schema)
    event_dict = next(reader)
    return event_dict

consumer = KafkaConsumer(
    bootstrap_servers=['localhost:19092', 'localhost:19091', 'localhost:19090'],
    value_deserializer=avro_decoder,
    group_id="Coins",
    auto_offset_reset="earliest",
)

consumer.subscribe(["criptomonedas"])

while True:
    info_dict = consumer.poll(timeout_ms=5000)
    for topic_partition, messages in info_dict.items():
        for message in messages:
            mensaje = message.value
            print(avro_decoder(mensaje))
    time.sleep(15)
