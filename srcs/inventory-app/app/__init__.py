from flask import Flask
from sqlalchemy.exc import OperationalError
from .config import Config
from .models import db
import time

def wait_for_db(max_retries=10, delay=2):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            db.engine.connect()
            print(f"Database connected on attempt {attempt + 1}")
            return True
        except OperationalError as e:
            print(f"Database not ready (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(delay)
            else:
                raise
    return False

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    from .routes.movies import movies_bp
    from .routes.health import health_bp

    app.register_blueprint(movies_bp)
    app.register_blueprint(health_bp)

    db.init_app(app)
    with app.app_context():
        wait_for_db()
        db.create_all()

    @app.errorhandler(Exception)
    def handle_exception(e):
        if hasattr(e, "code"):
            print(f"Error: {e}, Code: {e.code}")
            if hasattr(e, "description"):
                return {"error": e.description}, e.code
            return {"error": "An error occurred"}, e.code
        return {"error": "Internal Server Error", "message": str(e)}, 500

    return app


import os

def get_env_variable(name, cast_type=str):
    """
    Retrieves an environment variable. 
    Raises a Detailed RuntimeError if the variable is missing.
    """
    
    value = os.getenv(name)
    if name is None:
        raise RuntimeError(f"CRITICAL ERROR: Environment variable '{name}' is not set.")
    try:
        return cast_type(value)
    except ValueError:
        raise RuntimeError(f"CRITICAL ERROR: Variable '{name}' must be of type {cast_type.__name__}.")