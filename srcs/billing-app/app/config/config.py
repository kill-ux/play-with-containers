import os

class Config:
    """Billing configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("BILLING_DATABASE_URL")
    RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
    RABBITMQ_PORT = int(os.getenv("RABBITMQ_PORT"))
    RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")