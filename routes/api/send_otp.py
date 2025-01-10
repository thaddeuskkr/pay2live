import requests
import secrets
import os
from flask import request, make_response
from app import app, ready, users
from classes import User


@app.route("/api/send_otp", methods=["POST"])
def otp():
    data = request.get_json()
    required_fields = ["phone"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response({"error": f"Missing required fields: {missing_keys}"}, 400)
    phone: str = data.get("phone")
    if (len(phone) != 8) or (not phone.isdigit()):
        response = make_response(
            {
                "phone": phone,
                "message": "Invalid phone number",
            },
            400,
        )
        return response
    otp = str(secrets.randbelow(10**6)).rjust(6, "0")
    if not ready:
        response = make_response(
            {
                "message": "Service is not ready. Please try again later.",
            },
            500,
        )
        return response
    userC = User(phone=phone, otp=otp)
    if users.find_one({"phone": phone}):
        users.update_one({"phone": phone}, {"$set": {"otp": otp}})
    else:
        users.insert_one(userC.to_dict())
    request_response = requests.post(
        "https://develop.tkkr.dev/otp",
        json={"to": f"65{phone}", "from": "pay2live", "otp": otp},
        headers={"Authorization": os.environ["OTP_TOKEN"]},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "phone": phone,
                "message": f"OTP sent to {phone}",
            },
            200,
        )
        return response
    else:
        response = make_response(
            {
                "phone": phone,
                "message": "Failed to send OTP. Please try again later.",
            },
            500,
        )
        return response
