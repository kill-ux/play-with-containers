from dotenv import load_dotenv
load_dotenv()

import os

from app import create_app, get_env_variable

app = create_app()

HOST = get_env_variable("GATEWAY_HOST")
PORT = get_env_variable("GATEWAY_PORT")
DEBUG = get_env_variable("GATEWAY_DEBUG").lower() in ("true", "1", "t")

if __name__ == "__main__":
    app.run(debug=DEBUG, host=HOST, port=PORT)
    