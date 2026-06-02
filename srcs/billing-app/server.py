import threading
from dotenv import load_dotenv
load_dotenv()

from app import create_app, get_env_variable
from app.worker import start_order_consumer

app = create_app()

if __name__ == "__main__":
    HOST = get_env_variable("BILLING_HOST")
    PORT = get_env_variable("BILLING_PORT", int)
    
    # Start RabbitMQ consumer in a separate thread
    worker_thread = threading.Thread(target=start_order_consumer, args=(app,), daemon=True)
    worker_thread.start()

    app.run(host=HOST, port=PORT)