from dotenv import load_dotenv
from waitress import serve
load_dotenv()

import os

from app import create_app, get_env_variable

app = create_app()

PORT = get_env_variable("APIGATEWAY_PORT")

if __name__ == "__main__":
    serve(app,listen=f"*:{PORT}")
    