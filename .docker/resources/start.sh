#!/bin/bash

set -e

echo "[INFO] Esperando a RabbitMQ en $RABBITMQ_HOST:$RABBITMQ_PORT..."

# Espera hasta que el puerto esté disponible
while ! nc -z "$RABBITMQ_HOST" "$RABBITMQ_PORT"; do
  sleep 1
done

# Arranca FastAPI y el consumidor en segundo plano
uvicorn interfaces.http.main:app --host 0.0.0.0 --port 8000 --reload &

# Ejecuta los consumidores (puedes agregar más si lo necesitas)
python main_consumer.py
