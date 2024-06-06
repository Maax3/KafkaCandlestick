from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from pyspark.sql.streaming import DataStreamWriter

#::::ESTE ARCHIVO SIMULA 2 CONSUMIDORES MEDIANTE PYSPARK:::

SCHEMA_URL = "http://localhost:8081/subjects/criptomonedas/versions/latest"
schema = json.loads(fetch_schema(SCHEMA_URL)) #convierte str a json

# Crear el SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .getOrCreate()

# Definir el esquema Avro como un esquema de Spark
avro_schema = StructType([
    StructField("nombre", StringType(), True),
    StructField("valor", FloatType(), True),  # Añadir campos según el esquema Avro real
    StructField("timestamp", StringType(), True)  # Añadir campos según el esquema Avro real
])

# Leer datos desde Kafka
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "localhost:19092,localhost:19091,localhost:19090") \
  .option("subscribe", "criptomonedas") \
  .option("startingOffsets", "earliest") \
  .load()

# Convertir el valor binario a cadena y luego a un DataFrame JSON
df = df.selectExpr("CAST(value AS STRING) as json_str")

# Convertir la cadena JSON a columnas
df = df.withColumn("data", from_json(col("json_str"), avro_schema)).select("data.*")

# Configuración de InfluxDB
influxdb_client = InfluxDBClient(url="http://localhost:8086", token="your_token", org="your_org")
bucket = "your_bucket"
write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

# Función para escribir en InfluxDB
def write_to_influxdb(row):
    point = Point("criptomonedas") \
        .tag("nombre", row.nombre) \
        .field("valor", row.valor) \
        .time(row.timestamp, WritePrecision.NS)
    write_api.write(bucket=bucket, record=point)

# Convertir a RDD y luego escribir en InfluxDB
def foreach_batch_function(df, epoch_id):
    df.foreach(write_to_influxdb)

# Ejecutar el streaming
query = df.writeStream \
    .foreachBatch(foreach_batch_function) \
    .outputMode("append") \
    .start()

query.awaitTermination()
