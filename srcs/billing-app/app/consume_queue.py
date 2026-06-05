import os
import pika
import json

from app.orders import create_order

RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASS')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')


def consume_and_store_order(engine):
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            RABBITMQ_HOST,
            RABBITMQ_PORT,
            '/',
            credentials
        )
    )
    print("[5] Connected to RabbitMQ successfully!", flush=True)
    channel = connection.channel()
    print("[6] Channel created", flush=True)
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True, arguments={"x-queue-type": "quorum"})
    print(f"[7] Queue '{RABBITMQ_QUEUE}' declared", flush=True)

    def callback(ch, method, properties, body):
        print(f" [.] received: {body.decode()}")
        try:
            new_order = json.loads(body.decode())
            create_order(engine, new_order)
            print(" [x] created new order")
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f" [-] error: {e}")

    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback
    )
    print("[*] billing app started cunsuming msgs...", flush=True)
    channel.start_consuming()