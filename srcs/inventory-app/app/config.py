import os


class Config:
    """Base configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv("INVENTORY_MOVIES_DATABASE_URL")
    