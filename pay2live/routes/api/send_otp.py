import requests
import secrets
import os
from flask import request, make_response
from pay2live import app, ready, logins


@app.route("/api/send_otp", methods=["POST"])
def otp():
    data = request.get_json()
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
    logins.update_one({"phone": phone}, {"$set": {"otp": otp}}, upsert=True)
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
