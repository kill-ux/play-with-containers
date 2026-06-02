import pika
import json
import os
from .models.models import db, Order

def start_order_consumer(app):
    """Background worker to consume order messages from RabbitMQ"""
    print("start")
    user = os.getenv("RABBITMQ_USER")
    password = os.getenv("RABBITMQ_PASS")
    credentials = pika.PlainCredentials(user, password)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=app.config['RABBITMQ_HOST'],
        port=app.config['RABBITMQ_PORT'],
        credentials=credentials
    ))
    print("connect")
    channel = connection.channel()
    print("channel")
    
    print(app.config['RABBITMQ_QUEUE'])
    channel.queue_declare(queue=app.config['RABBITMQ_QUEUE'], durable=True, arguments={"x-queue-type": "quorum"})
    print("RABBITMQ_QUEUE")

    def callback(ch, method, properties, body):
        with app.app_context():
            try:
                data = json.loads(body)
                # Create the order in the Billing DB using required fields
                new_order = Order(
                    user_id=str(data['user_id']),
                    number_of_items=int(data['number_of_items']),
                    total_amount=float(data['total_amount'])
                )
                db.session.add(new_order)
                db.session.commit()
                print(f" [x] Order recorded for User {data['user_id']}")
            except Exception as e:
                print(f" [!] Error processing message: {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=app.config['RABBITMQ_QUEUE'], on_message_callback=callback)
    print(f" [*] Waiting for messages in {app.config['RABBITMQ_QUEUE']}. To exit press CTRL+C")
    channel.start_consuming()