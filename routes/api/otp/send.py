import requests
import secrets
from flask import request, make_response
from app import app, ready, users, whatsapp_api_auth, whatsapp_api_url
import html


@app.route("/api/otp/send", methods=["POST"])
def send_otp():
    data = request.get_json()
    required_fields = ["phone"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    phone: str = data.get("phone")
    if (len(phone) != 8) or (not phone.isdigit()):
        response = make_response(
            {
                "phone": html.escape(phone),
                "message": "Invalid phone number",
            },
            400,
        )
        return response
    otp = str(secrets.randbelow(10**6)).rjust(6, "0")
    if not ready:
        response = make_response(
            {
                "message": "The OTP service is not ready. Please try again later.",
            },
            500,
        )
        return response
    db_user = users.find_one({"phone": phone})
    if db_user:
        if not db_user["active"]:
            response = make_response(
                {
                    "phone": html.escape(phone),
                    "message": "Your account has been deactivated. Please contact support.",
                },
                400,
            )
            return response
        users.update_one({"phone": phone}, {"$set": {"otp": otp}})
    else:
        users.insert_one(
            {
                "phone": phone,
                "first_name": None,
                "last_name": None,
                "email": None,
                "gender": None,
                "nric": None,
                "role": "patient",
                "address1": None,
                "address2": None,
                "address3": None,
                "address4": None,
                "session_token": None,
                "otp": otp,
                "otp2": None,
                "admin": False,
                "registered": False,
                "active": True,
            }
        )
    request_response = requests.post(
        f"{whatsapp_api_url}",
        json={
            "to": f"65{phone}",
            "from": "pay2live",
            "message": f"*{otp}* is your one-time password to log in to *pay2live*. Do not share this OTP with anyone.",
        },
        headers={"Authorization": whatsapp_api_auth},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "phone": html.escape(phone),
                "message": f"OTP sent to {html.escape(phone)}",
            },
            200,
        )
        return response
    else:
        response = make_response(
            {
                "phone": html.escape(phone),
                "message": f"Failed to send OTP to {html.escape(phone)}. Please try again later.",
            },
            500,
        )
        return response
