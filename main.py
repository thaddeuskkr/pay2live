import os
import requests
import secrets
import shelve
from dotenv import load_dotenv
from flask import Flask, request, render_template, jsonify

load_dotenv()
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = os.getenv("DEBUG") == "True"

# TODO:
# - Move routes to different files (maybe under a routes/ folder) for better organisation
# - Set up account management
# - Consider using an actual database over shelve


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
    otp = secrets.randbelow(10**6)
    with shelve.open("logins") as logins:
        while otp in logins.values():
            otp = secrets.randbelow(10**6)
        logins[phone] = str(otp)
    requests.post(
        "https://develop.tkkr.dev/otp",
        json={"to": f"65{phone}", "from": "pay2live", "otp": otp},
        headers={"Authorization": os.getenv("OTP_TOKEN")},
    )
    return jsonify(
        {
            "status": 200,
            "phone": phone,
            "message": f"OTP sent to {phone}",
        }
    )


@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    otp = data.get("otp")
    phone = data.get("phone")
    with shelve.open("logins") as logins:
        if phone in logins.keys() and logins[phone] == otp:
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
                    "message": "Invalid OTP",
                }
            )


if __name__ == "__main__":
    app.run(debug=(os.getenv("DEBUG") == "True"))
