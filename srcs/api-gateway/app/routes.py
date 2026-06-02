from flask import Blueprint, request, jsonify
import requests
import os
import pika
import json

gateway_bp = Blueprint("gateway_bp", __name__)

INVENTORY_SERVICE_URL = os.getenv("INVENTORY_SERVICE_URL")
BILLING_SERVICE_URL = os.getenv("BILLING_SERVICE_URL")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))

API_MOVIES_URL = "/api/movies"
API_BILLING_URL = "/api/billing"
API_ORDERS_URL = "/api/orders"


@gateway_bp.route(API_MOVIES_URL + "/", methods=["GET", "POST", "DELETE"])
@gateway_bp.route(
    API_MOVIES_URL + "/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"]
)
def proxy_to_inventory(subpath=""):
    """Proxy endpoint to forward requests to the inventory service"""
    base_url = INVENTORY_SERVICE_URL.rstrip("/") + API_MOVIES_URL
    forwarded_url = f"{base_url}/{subpath}" if subpath else base_url

    try:
        resp = requests.request(
            method=request.method,
            url=forwarded_url,
            json=request.get_json() if request.is_json else None,
            params=request.args,
            allow_redirects=False,
        )

        excluded_headers = {
            "content-encoding",
            "content-length",
            "transfer-encoding",
            "connection",
        }

        headers = [
            (k, v)
            for k, v in resp.raw.headers.items()
            if k.lower() not in excluded_headers
        ]

        return resp.content, resp.status_code, headers
    except requests.exceptions.ConnectionError as e:
        print(f"Error connecting to inventory service: {e}")
        return {"error": "Inventory service is down"}, 503


# --- BILLING ROUTES ---
@gateway_bp.route(API_ORDERS_URL + "/", methods=["GET"])
def proxy_to_billing():
    """Directly proxy GET requests to the Billing Service"""
    # The billing app has /api/orders prefix
    forwarded_url = BILLING_SERVICE_URL.rstrip("/") + API_ORDERS_URL

    try:
        resp = requests.get(forwarded_url, params=request.args)
        return resp.content, resp.status_code
    except requests.exceptions.ConnectionError:
        return {"error": "Billing service is down"}, 503


@gateway_bp.route(API_BILLING_URL + "/", methods=["POST"])
def queue_order():
    """Send POST requests to RabbitMQ for asynchronous processing"""
    if not RABBITMQ_HOST:
        return {"error": "RabbitMQ host not configured"}, 500

    print("startttttttttttttttt")

    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    print(RABBITMQ_USER)
    print(RABBITMQ_PASS)
    print(RABBITMQ_HOST)
    print(RABBITMQ_QUEUE)


    try:
        print("conn start")
        # Connect to RabbitMQ
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST,port=RABBITMQ_PORT,credentials=credentials)
        )
        channel = connection.channel()
        print("conn established")


        # Ensure the queue exists
        channel.queue_declare(
            queue=RABBITMQ_QUEUE, durable=True, arguments={"x-queue-type": "quorum"}
        )

        # Publish the message
        message = request.get_json()
        channel.basic_publish(
            exchange="",
            routing_key=RABBITMQ_QUEUE,
            body=json.dumps(
                {
                    "user_id": message["user_id"],
                    "number_of_items": message["number_of_items"],
                    "total_amount": message["total_amount"],
                }
            ),
            properties=pika.BasicProperties(content_type="application/json")
        )
        connection.close()
        return {"message": "Order request accepted"}, 202

    except Exception as e:
        print(f"RabbitMQ Error: {type(e).__name__}: {str(e)}")
        return {"error": "Could not queue order"}, 503

