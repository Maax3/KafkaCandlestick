# Enlaces
* [EJEMPLO DE KAFKA (NullSafe (ES))](https://www.youtube.com/watch?v=MA-nxL14fr4&ab_channel=NullSafeArchitect)
* [KAFKA CONECTORES (NullSafe (ES))](https://www.youtube.com/watch?v=texXOyt-bPE&ab_channel=NullSafeArchitect)
* [KAFKA STREAMING (ES)](https://www.youtube.com/watch?v=8W6rFRk5SZE&list=PL2yjEVbRSX7WjbVrfG4b7VxuZa69Y5zrO&index=5&ab_channel=ParadigmaDigital)
* [SETUP KAFKA DOCKER (EN)](https://www.youtube.com/watch?v=L--VuzFiYrM&ab_channel=OttoCodes)
* [SETUP KAFKA SENCILLO EN DOCKER (ES)](https://www.youtube.com/watch?v=rhUuD0eA-EQ&ab_channel=DebuggeandoIdeas)
* [BASES KAFKA y EJEMPLOS REALES (EN)](https://www.youtube.com/watch?v=wmuuOYDaaBw&list=PLCh59G4US86oC5GnhYrSrKZKDoQbfzZLW&ab_channel=Upstash)
* [BASES DE KAFKA (RU)](https://www.youtube.com/watch?v=-AZOi3kP9Js)
* [LISTA DE VARIABLES KAFKA](https://docs.confluent.io/platform/current/installation/configuration/broker-configs.html?#)
* [DOCUMENTACION DE CONEXION CON DOCKER](https://docs.confluent.io/platform/current/kafka/multi-node.html#cp-multi-node)
* [COMO SE ESCRIBEN LAS VARIABLES DE KAFKA EN DOCKER](https://docs.confluent.io/platform/current/installation/docker/config-reference.html#config-reference)

# Apis
* cryptoCompare
* CoinMarketCap
* CoinGecko
* Bitfinex
* https://github.com/Crypto-toolbox/btfxwss

# Configuración

Crear un topico

Crear un consumidor (dentro del contenedor):

Crear un productor (dentro del contenedor): 
* cd /bin
```sh
  kafka-console-producer --bootstrap-server broker_1:9090 --topic mi_topico
```

Para verificar que el tópico tiene las configuraciones correctas:
* cd /bin
```sh
  kafka-topics --describe --zookeeper zookeeper:2181 --topic mi_topico
```

## Variables de entorno

#### KAFKA_LISTENERS - KAFKA_ADVERTISED_LISTENERS
``KAFKA_LISTENERS`` especifica dónde Kafka debe escuchar las conexiones entrantes, mientras que ``KAFKA_ADVERTISED_LISTENERS`` especifica qué endpoints deben ser anunciados a los clientes para que puedan establecer conexiones. La diferencia clave es que ``KAFKA_ADVERTISED_LISTENERS`` se utiliza para la comunicación externa con los clientes, mientras que ``KAFKA_LISTENERS`` se utiliza para la comunicación interna entre los componentes de Kafka.

# Tests
java.lang.IllegalArgumentException: requirement failed: inter.broker.listener.name must be a listener name defined in advertised.listeners. The valid options based on currently configured listeners are RED_INTERNA,RED_EXTERNA

[df](https://docs.confluent.io/platform/current/kafka/multi-node.html#cp-multi-node)
https://docs.confluent.io/platform/current/installation/docker/config-reference.html#config-reference

```yml
---
version: '3'
services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    hostname: zookeeper
    container_name: zookeeper
    ports:
      - "2181:2181"
    networks:
      - kafka_net
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
      #ZOOKEEPER_DATA_DIR: /var/lib/zookeeper/data
    #volumes:
     # - ./zookeeper-data:/var/lib/zookeeper/data

  broker_1:
    image: confluentinc/cp-kafka:latest
    hostname: broker_1
    container_name: broker_1
    depends_on:
      - zookeeper
    ports:
      - "9090:9090"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT #plaintext = sin cifrado
      KAFKA_ADVERTISED_LISTENERS: RED_INTERNA://broker_1:29090,RED_EXTERNA://localhost:9090
      KAFKA_LISTENERS: RED_INTERNA://:29090, RED_EXTERNA://:9090 #ruta de escucha para Kafka
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker1:/var/lib/kafka/data

  broker_2:
    image: confluentinc/cp-kafka:latest
    hostname: broker_2
    container_name: broker_2
    depends_on:
      - zookeeper
    ports:
      - "9091:9091"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: RED_INTERNA://broker_2:29091,RED_EXTERNA://localhost:9091
      KAFKA_LISTENERS: RED_INTERNA://:29091, RED_EXTERNA://:9091 #ruta de escucha para Kafka
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker2:/var/lib/kafka/data

  broker_3:
    image: confluentinc/cp-kafka:latest
    hostname: broker_3
    container_name: broker_3
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: RED_INTERNA://broker_3:29092,RED_EXTERNA://localhost:9092 #ruta para clientes
      KAFKA_LISTENERS: RED_INTERNA://:29092, RED_EXTERNA://:9092 #ruta de escucha para Kafka
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker3:/var/lib/kafka/data

networks:
  kafka_net:
    name: network_kafka_conexion
  
```
  
