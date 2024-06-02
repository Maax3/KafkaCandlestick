# Entorno
  ```python
  python -m venv kafka
  source venv/bin/activate
  pip list
  ```

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
* [Conexion con Azure Databricks](https://www.youtube.com/watch?v=Sa3ubGXvT44&ab_channel=NextGenLearning)
* [Información sobre Kafka SQL o KSQL y sus diferencias con Kafka Stream API](https://es.slideshare.net/KaiWaehner/kafka-streams-vs-ksql-for-stream-processing-on-top-of-apache-kafka-142127337)

# Configuración de conexión
* [PART1](https://rmoff.net/2018/08/02/kafka-listeners-explained/)
* [PART2](https://www.confluent.io/blog/kafka-client-cannot-connect-to-broker-on-aws-on-docker-etc/?utm_source=github&utm_medium=rmoff&utm_campaign=ty.community.con.rmoff-listeners&utm_term=rmoff-devx)

# Apis
* cryptoCompare
* CoinMarketCap
* CoinGecko
* Bitfinex
* https://github.com/Crypto-toolbox/btfxwss

# Configuración

Ver tu IP pública

```sh
curl ifconfig.me
```

Crear un consumidor (dentro del contenedor):

* cd /bin
```sh
  kafka-console-consumer --bootstrap-server broker_3:29092 --topic mi_topico
```

Crear un productor (dentro del contenedor): 
* cd /bin
```sh
  kafka-console-producer --bootstrap-server broker_1:29090 --topic mi_topico
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
      - "19090:19090"
      - "29090:29090"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT,RED_LOCAL:PLAINTEXT #plaintext = sin cifrado
      KAFKA_ADVERTISED_LISTENERS: 
        RED_EXTERNA://adb-3223500186722566.6.azuredatabricks.net:9090,
        RED_INTERNA://broker_1:29090,
        RED_LOCAL://localhost:19090
      KAFKA_LISTENERS: 
        RED_EXTERNA://:9090, 
        RED_INTERNA://broker_1:29090, 
        RED_LOCAL://broker_1:19090
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker1:/var/lib/kafka/data
      - ./server-logs/kafka-broker1:/var/log/kafka

  broker_2:
    image: confluentinc/cp-kafka:latest
    hostname: broker_2
    container_name: broker_2
    depends_on:
      - zookeeper
    ports:
      - "9091:9091"
      - "29091:29091"
      - "19091:19091"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 2
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT,RED_LOCAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: 
        RED_EXTERNA://adb-3223500186722566.6.azuredatabricks.net:9091,
        RED_INTERNA://broker_2:29091,
        RED_LOCAL://localhost:19091
      KAFKA_LISTENERS: 
        RED_EXTERNA://:9091, 
        RED_INTERNA://broker_2:29091, 
        RED_LOCAL://broker_2:19091
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker2:/var/lib/kafka/data
      - ./server-logs/kafka-broker2:/var/log/kafka

  broker_3:
    image: confluentinc/cp-kafka:latest
    hostname: broker_3
    container_name: broker_3
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
      - "19092:19092"
      - "29092:29092"
    networks:
      - kafka_net
    environment:
      KAFKA_BROKER_ID: 3
      KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'
      KAFKA_INTER_BROKER_LISTENER_NAME: RED_INTERNA
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: RED_INTERNA:PLAINTEXT,RED_EXTERNA:PLAINTEXT,RED_LOCAL:PLAINTEXT
      KAFKA_ADVERTISED_LISTENERS: 

        RED_INTERNA://broker_3:29092,
        RED_LOCAL://localhost:19092
      KAFKA_LISTENERS: 
        RED_EXTERNA://:9092, 
        RED_INTERNA://broker_3:29092, 
        RED_LOCAL://broker_3:19092
      KAFKA_NUM_PARTITIONS: 2
      KAFKA_DEFAULT_REPLICATION_FACTOR: 3
      KAFKA_MIN_INSYNC_REPLICAS: 2
      KAFKA_LOG_DIRS: /var/lib/kafka/data
    volumes:
      - ./logs/kafka-logs-broker3:/var/lib/kafka/data
      - ./server-logs/kafka-broker3:/var/log/kafka

  kafka-ui:
    image: provectuslabs/kafka-ui:latest
    hostname: kafka-ui
    container_name: kafka-ui
    ports:
      - "8080:8080"
    networks:
      - kafka_net
    depends_on:
      - broker_1
      - broker_2
      - broker_3
      - zookeeper
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: broker_1:29090,broker_2:29091,broker_3:29092
      KAFKA_CLUSTERS_0_ZOOKEEPER: zookeeper:2181

networks:
  kafka_net:
    name: network_kafka_conexion
  

```

# Consumidores

Existen conectores específicos de Kafka para InfluxDB, como Kafka Connect, que permiten la ingesta continua de datos desde tópicos de Kafka hacia InfluxDB sin necesidad de escribir código personalizado.

- Un grupo de consumidores es un grupo que funciona en conjunto para procesar los mensajes de una o varias particiones de un topico determinado. Cada particion en el topico
puede ser asignada a un solo consumidor. TLDR: los consumidores de un mismo grupo de consumidores no pueden pisarse entre ellos, pero si si se trata de un grupo diferente de consumidores. El grupo de consumidores se establece con "group.id"

Kafka tiene 3 patrones de consumo:
 - Exactly-Once: Garantiza que cada mensaje se procese exactamente una vez, eliminando los duplicados.
 - At-most-once: Garantiza que cada mensaje se envie al consumidor, pero no asegura que este lo haya procesado
 - At-Least-Once: Garantiza que cada mensaje se envie al consumidor y que se procese al menos una vez, pero puede provocar duplicados. 

Hay dos valores principales que se pueden usar para auto_offset_reset:
 - earliest: Esto significa que el consumidor comenzará a leer desde el offset más temprano disponible para el topic al que está suscrito. En otras palabras, si no hay un offset inicial disponible (porque es la primera vez que el consumidor se une al grupo o porque el offset inicial se ha perdido), el consumidor comenzará a leer desde el principio del registro de transacciones (commit log) del topic.
 - latest: Esto significa que el consumidor comenzará a leer desde el offset más reciente disponible para el topic al que está suscrito. Si no hay un offset inicial disponible, el consumidor comenzará a leer desde el final del registro de transacciones del topic.

# Productor y particiones

- Cada particion puede ser interpretada como una unidad independiente de streaming de mensajes. Tanto productores como consumidores pueden escribir y leer datos de forma concurrente.
- Los offsets son únicos respecto a la partición. Es decir, si existen 2 particiones en un topico puede haber mensajes con un offset con el mismo valor.
- Los mensajes se insertan de forma secuencial en una partición garantizando un orden conforme al valor del offset.
- Una vez asignado el offset, este se vuelve inmutable.


### ¿Qué es la serialización y cómo funciona?
**Serialización** es el proceso de convertir un objeto o estructura de datos en un formato que puede ser almacenado o transmitido y luego reconstruido (deserializado) más tarde. En términos simples, la serialización convierte datos en una secuencia de bytes, mientras que la deserialización convierte esa secuencia de bytes de vuelta a su formato original.

### ¿Por qué Kafka necesita serializar datos cuando un productor envía mensajes?
- Respuesta corta: Por eficiencia

**Por la compatibilidad:** 
En Kafka, los datos deben ser convertidos a un formato binario antes de ser enviados a los brokers. 

**Por la Interoperabilidad:** 
- Diferentes sistemas y lenguajes de programación pueden interactuar con Kafka. La serialización garantiza que los datos enviados por un productor puedan ser interpretados correctamente por cualquier consumidor, independientemente del lenguaje de programación utilizado.

**Por la Integridad de los datos:**
- Al serializar los datos, se asegura que la estructura y el contenido de los datos se mantengan íntegros durante el proceso de transmisión y almacenamiento.

### Líderes y Réplicas 

En Kafka, cada partición tiene un líder y puede tener varias réplicas. El líder es el responsable de manejar todas las lecturas y escrituras de esa partición. Las réplicas actúan como copias de seguridad. Si un broker que actúa como líder falla, uno de los brokers que contiene una réplica puede asumir el rol de líder, garantizando la continuidad del servicio. Las replicas líder son las que tienen la carga de trabajo, si existe un rendimiento pobre hay que comprobar que los líderes esten correctamente distribuidos entre los brokers.

Kafka intenta distribuir siempre las particiones de un tópico de manera equilibrada entre los brokers para balancear la carga. Así, un broker puede ser líder de varias particiones de diferentes tópicos o puedes tener múltiples brokers que son líderes de una sola partición dentro de un unico topico.

Las replicas denominadas "seguidores" mandan peticiones a la partición líder de forma periodica para hacer el backup de los datos. Al hacerse de forma periodica y asincrona, puede existir un caso donde no todas las réplicas tengan los datos completos del líder en el momento de que este 'caiga' o 'muera'. Para solucionar esto existe el follower "ISR", que en esencia, es un parametro dentro de kafka llamado "min.insync.replicas" que permite cambiar el modo de escritura de asincrono a sincrono. De modo que, al mismo tiempo que se escriben los datos en el líder, se escriben en las réplicas ISR asignadas. 

- Por ejemplo, si ponemos min.insync.replicas = 3, los datos se escribirán de forma sincrona en la particion líder y en 2 de sus réplicas "seguidoras".
- El numero minimo de replicas sincronas debe ser igual o menor al numero de replicas que tengas sin contar el lider. En caso contrario, podria haber conflicto de escritura y en el almacenamiento de datos.

Además de establecer el min.insync también hay que configurar el envio de mensajes que hace el productor, en este caso, habria que establecer el parámetro acks a "all". Acks tiene 3 variantes:
 - 0 = Sin comprobación de que el mensaje se ha escrito correctamente.
 - 1 = El mensaje ha llegado con éxtio al líder.
 - all = Se ha completo con éxito en todas las replicas ISR + líder.

## A la hora de definir la particion en el Productor:
 - Puedes especificar que sea "Round-Robin" para que los mensajes se repartan entre las particiones existentes
 - Puedes especificar una particion de forma explicita, por ej "Productor 1 que envie al topic A - particion 0"
 - Por key-hash. Se utiliza para distribuir los mensajes de forma equitativa entre las diferentes particiones y al mismo tiempo garantiza que todos los mensajes con la misma clave sean enviados a la misma partición. Ejemplo:

```python
  producer.produce('transacciones', key='usuario1', value='Compra por $100', callback=delivery_report)
  producer.produce('transacciones', key='usuario2', value='Compra por $50', callback=delivery_report)
  producer.produce('transacciones', key='usuario1', value='Devolución por $20', callback=delivery_report)
  producer.produce('transacciones', key='usuario3', value='Compra por $200', callback=delivery_report)
```

Si tenemos 3 particiones; Kafka podría distribuirlos tal que así:
 - Particion 0 (usuario1 y sus 2 mensajes)
 - Particion 1 (usuario2 y su mensaje)
 - Particion 2 (usuario3 y su mensaje)

**Como funciona el key-hash internamente:**

Kafka toma la clave del mensaje, calcula su hash y luego aplica una operación de módulo con el número de particiones del topic (hash(key) % num_partitions). El resultado de esta operación es el índice de la partición a la que se enviará el mensaje



::::::::::OPTIMIZACION:::::::::

Zero-Copy en Kafka es una técnica de optimización que permite transferir datos entre productores y consumidores sin copiarlos de un búfer de memoria a otro, lo que mejora significativamente el rendimiento del sistema.

  
