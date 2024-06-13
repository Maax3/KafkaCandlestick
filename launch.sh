#!/bin/bash
# Damos permisos y lanzamos el script para crear el esquema en el schema-registry de docker
chmod +x ./scripts/avro_schema.sh
./scripts/avro_schema.sh
# Lanzamos el productor y consumidor
python ./scripts/productor_avro.py &
python ./scripts/consumidor_avro_hilos.py