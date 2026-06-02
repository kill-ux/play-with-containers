from flask import Flask
from .config.config import Config
from .models.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    from .controllers.orders import billing_bp
    app.register_blueprint(billing_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

import os
def get_env_variable(name, cast_type=str):
    value = os.getenv(name)
    try:
        if value is None:
            raise RuntimeError(f"CRITICAL ERROR: Environment variable '{name}' is not set.")
        return cast_type(value)
    except ValueError:
        raise RuntimeError(f"CRITICAL ERROR: Variable '{name}' must be of type {cast_type.__name__}.")