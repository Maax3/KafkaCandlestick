#!/bin/bash
chmod +x ./scripts/avro_schema.sh
./scripts/avro_schema.sh
python ./scripts/productor_avro.py