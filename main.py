import os
import requests
import secrets
import typing
import logging
import threading
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

# TODO:
# - Move routes to different files (maybe under a routes/ folder) for better organisation
# - Set up account management
# - Consider using an actual database over shelves

load_dotenv()

# Check environment variables
debug = os.environ["DEBUG"].lower() == "true"
try:
    otp_token = os.environ["OTP_TOKEN"]
    mongo_url = os.environ["MONGODB_CONNECTION_URL"]
except KeyError as e:
    raise ValueError(f"Required environment variable {e} is not set")

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="pay2live.log", level=logging.DEBUG if debug else logging.INFO
)

# Initialise Flask application
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = debug

# Initialise MongoDB client using database "pay2live"
mongo_client: MongoClient[dict[str, typing.Any]] = MongoClient(
    mongo_url, serverSelectionTimeoutMS=5000
)
db = mongo_client[f"pay2live{'_dev' if debug else ''}"]
logins = db["logins"]


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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/otp", methods=["POST"])
def otp():
    data = request.get_json()
    phone = data.get("phone")
    otp = str(secrets.randbelow(10**6)).rjust(6, "0")
    if not ready:
        return jsonify(
            {
                "status": 500,
                "message": "Service is not ready. Please try again later.",
            }
        )
    logins.update_one({"phone": phone}, {"$set": {"otp": otp}}, upsert=True)
    response = requests.post(
        "https://develop.tkkr.dev/otp",
        json={"to": f"65{phone}", "from": "pay2live", "otp": otp},
        headers={"Authorization": os.getenv("OTP_TOKEN")},
    )
    if response.status_code == 200:
        return jsonify(
            {
                "status": 200,
                "phone": phone,
                "message": f"OTP sent to {phone}",
            }
        )
    else:
        return jsonify(
            {
                "status": 500,
                "message": "Failed to send OTP. Please try again later.",
            }
        )


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    otp = data.get("otp")
    phone = data.get("phone")
    login = db["logins"].find_one({"phone": phone})
    if login is None:
        return jsonify(
            {
                "status": 400,
                "phone": phone,
                "message": "No OTP has been sent for this phone number",
            }
        )
    elif login["otp"] == otp:
        return jsonify(
            {
                "status": 200,
                "phone": phone,
                "message": "OTP verified",
            }
        )
    else:
        return jsonify(
            {
                "status": 400,
                "phone": phone,
                "message": "Invalid OTP",
            }
        )


if __name__ == "__main__":
    app.run(debug=debug)
