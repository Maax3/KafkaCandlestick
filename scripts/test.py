import os
from kafka import KafkaConsumer
import fastavro
from fastavro.schema import load_schema
from io import BytesIO

# Ruta del esquema Avro
schema_path = os.path.join(os.path.dirname(__file__), 'esquema_avro.avsc')
avro_schema = load_schema(schema_path)

consumer = KafkaConsumer(
    'criptomonedas',
    bootstrap_servers=['localhost:19092', 'localhost:19091', 'localhost:19090'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='Coins',
)


# Función para deserializar mensajes Avro
def deserialize_avro_message(message_value, schema):
    bytes_reader = BytesIO(message_value)
    reader = fastavro.reader(bytes_reader, schema)
    for mensaje in reader:
        return mensaje['nombre']

# Consumir mensajes
for message in consumer:
    message_value = message.value
    avro_record = deserialize_avro_message(message_value, avro_schema)
    print(avro_record)
