from dotenv import load_dotenv
load_dotenv()

from app import create_app, get_env_variable

HOST = get_env_variable("INVENTORY_HOST")
PORT = get_env_variable("INVENTORY_PORT")

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
