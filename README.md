# Enlaces
* [EJEMPLO DE KAFKA (NullSafe (ES))](https://www.youtube.com/watch?v=MA-nxL14fr4&ab_channel=NullSafeArchitect)
* [KAFKA CONECTORES (NullSafe (ES))](https://www.youtube.com/watch?v=texXOyt-bPE&ab_channel=NullSafeArchitect)
* [KAFKA STREAMING (ES)](https://www.youtube.com/watch?v=8W6rFRk5SZE&list=PL2yjEVbRSX7WjbVrfG4b7VxuZa69Y5zrO&index=5&ab_channel=ParadigmaDigital)
* [SETUP KAFKA DOCKER (EN)](https://www.youtube.com/watch?v=L--VuzFiYrM&ab_channel=OttoCodes)
* [SETUP KAFKA SENCILLO EN DOCKER (ES)](https://www.youtube.com/watch?v=rhUuD0eA-EQ&ab_channel=DebuggeandoIdeas)
* [BASES KAFKA y EJEMPLOS REALES (EN)](https://www.youtube.com/watch?v=wmuuOYDaaBw&list=PLCh59G4US86oC5GnhYrSrKZKDoQbfzZLW&ab_channel=Upstash)
* [BASES DE KAFKA (RU)](https://www.youtube.com/watch?v=-AZOi3kP9Js)

# Apis
* cryptoCompare
* CoinMarketCap
* CoinGecko
* Bitfinex
* https://github.com/Crypto-toolbox/btfxwss

# Tests
[html](https://docs.confluent.io/platform/current/installation/docker/installation.html)
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
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker_1:29090,PLAINTEXT_HOST://localhost:9090
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

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
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker_2:29091,PLAINTEXT_HOST://localhost:9091
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

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
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker_3:29092,PLAINTEXT_HOST://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 3
      KAFKA_GROUP_INITIAL_REBALANCE_DELAY_MS: 0
      KAFKA_CONFLUENT_LICENSE_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_CONFLUENT_BALANCER_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_TRANSACTION_STATE_LOG_MIN_ISR: 1
      KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR: 1

networks:
  kafka_net:
    name: network_kafka_conexion
  
