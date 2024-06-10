#!/bin/bash
# Damos permisos y lanzamos el script para crear el esquema en el esquema-registry de docker
chmod +x ./scripts/avro_schema.sh
./scripts/avro_schema.sh
# Lanzamos el productor
python ./scripts/productor_avro.py 
#&
#python ./scripts/consumidor_avro.py