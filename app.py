import os
import typing
import threading
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from flask import Flask

load_dotenv(override=True)

# Check environment variables
try:
    debug = os.environ["DEBUG"].lower() == "true"
except KeyError:
    debug = False

try:
    mongo_url = os.environ["MONGODB_CONNECTION_URL"]
    whatsapp_api_url = os.environ["WHATSAPP_API_URL"]
    whatsapp_api_auth = os.environ["WHATSAPP_API_AUTH"]
    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_username = os.environ["SMTP_USERNAME"]
    smtp_password = os.environ["SMTP_PASSWORD"]
    smtp_sender = os.environ["SMTP_SENDER"]
except KeyError as e:
    raise ValueError(f"Required environment variable {e} is not set")

# Initialise Flask application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = debug

# Initialise MongoDB client using database "pay2live"
mongo_client: MongoClient[dict[str, typing.Any]] = MongoClient(
    mongo_url, serverSelectionTimeoutMS=5000
)
db = mongo_client[f"pay2live{'_dev' if debug else ''}"]
users = db["users"]
queue = db["queue"]
appointments = db["appointments"]
shop = db["shop"]
carts = db["carts"]
orders = db["orders"]
tickets = db["tickets"]


# Check if MongoDB is ready every minute
def check_mongodb_connection():
    global ready
    try:
        mongo_client.admin.command("ping")
    except ConnectionFailure:
        print("Database not available")
        ready = False
    else:
        ready = True


thread = threading.Timer(60.0, check_mongodb_connection)
thread.start()
check_mongodb_connection()

from routes import *

if __name__ == "__main__":
    app.run(debug=debug)
