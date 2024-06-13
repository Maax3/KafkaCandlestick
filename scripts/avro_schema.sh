#!/bin/bash
while ! curl -s http://localhost:8081/subjects; do
  echo "El contenedor aún se esta iniciando..."
  sleep 30
done
echo -e "\nEsquema creado con exito!"
curl -X POST -H "Content-Type: application/vnd.schemaregistry.v1+json" --data '{"schema": "{\"type\":\"record\",\"name\":\"CryptoCurrency\",\"fields\":[{\"name\":\"nombre\",\"type\":\"string\"},{\"name\":\"bid\",\"type\":\"double\"},{\"name\":\"bid_size\",\"type\":\"double\"},{\"name\":\"ask\",\"type\":\"double\"},{\"name\":\"ask_size\",\"type\":\"double\"},{\"name\":\"daily_change\",\"type\":\"double\"},{\"name\":\"daily_change_percentage\",\"type\":\"double\"},{\"name\":\"precio_ultimo\",\"type\":\"double\"},{\"name\":\"volume\",\"type\":\"double\"},{\"name\":\"precio_maximo\",\"type\":\"double\"},{\"name\":\"precio_minimo\",\"type\":\"double\"}]}"}' http://localhost:8081/subjects/criptomonedas/versions