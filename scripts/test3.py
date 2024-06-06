def ver_mensajes(consumer):
    for message in consumer:
        try:
            mensaje = avro_decoder(message.value)
            print(f"El {consumer.config['client_id']} se ha ocupado del: {mensaje}\n")
            
            tiempo_actual = dt.datetime.utcnow()
            timestamp = tiempo_actual.isoformat() + 'Z'  # Añadir 'Z' para indicar que es en formato UTC
            registro = (
                Point("criptomonedas")
                .tag("Moneda", mensaje['nombre'])
                .field("Precio", mensaje['precio_ultimo'])
                .time(timestamp)
            )
            
            write_api.write(bucket=bucket, org=os.getenv("ORG"), record=registro)
        except Exception as e:
            print(f"Error procesando el mensaje: {e}")
