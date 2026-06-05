from dotenv import load_dotenv
from waitress import serve
load_dotenv()

from app import create_app, get_env_variable

PORT = get_env_variable("INVENTORY_APP_PORT")

app = create_app()

if __name__ == "__main__":
    serve(app, listen=f"*:{PORT}")
