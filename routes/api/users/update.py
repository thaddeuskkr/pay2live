import re
import secrets
from flask import request, make_response
import requests
from app import app, users, otp_token, whatsapp_api_url
from util import validate_nric
import html


@app.route("/api/users/update", methods=["POST"])
def update_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    required_fields = [
        "first_name",
        "last_name",
        "phone",
        "email",
        "gender",
        "nric",
        "address1",
        "address2",
        "address4",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    phone: str = data.get("phone")
    email: str = data.get("email")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    address1: str = data.get("address1")
    address2: str = data.get("address2")
    address3: str = data.get("address3")
    address4: str = data.get("address4")
    otp: str = data.get("otp")

    if not otp or len(otp) != 6:
        otp = str(secrets.randbelow(10**6)).rjust(6, "0")
        request_response = requests.post(
            f"{whatsapp_api_url}",
            json={
                "to": f"65{phone}",
                "from": "pay2live",
                "message": f"*{otp}* is your one-time password to finish updating your profile on *pay2live*. Do not share this OTP with anyone.",
            },
            headers={"Authorization": otp_token},
        )
        users.update_one({"session_token": session_token}, {"$set": {"otp2": otp}})
        if request_response.status_code == 200:
            response = make_response(
                {
                    "phone": html.escape(phone),
                    "message": f'An OTP has been sent to {html.escape(phone)} for verification. Enter the OTP and click "Apply Changes" to continue.',
                },
                418,
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

    if otp != user["otp2"]:
        return make_response(
            {"message": "Invalid OTP provided. Please try again."}, 400
        )
    else:
        users.update_one({"session_token": session_token}, {"$set": {"otp2": None}})

    if (
        len(first_name) < 1
        or len(last_name) < 1
        or len(phone) < 1
        or len(email) < 1
        or len(gender) <= 0
        or len(nric) < 1
        or len(address1) < 1
        or len(address2) < 1
        or len(address4) < 1
    ):
        return make_response({"message": "Invalid text in input fields"}, 400)
    if not re.match(r"^[a-zA-Z]+$", first_name):
        return make_response({"message": "Invalid first name"}, 400)
    if not re.match(r"^[a-zA-Z]+$", last_name):
        return make_response({"message": "Invalid last name"}, 400)
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return make_response({"message": "Invalid email address"}, 400)
    if not re.match(r"^\d{8}$", phone):
        return make_response({"message": "Invalid phone number"}, 400)
    if not re.match(r"^\d{6}$", address4):
        return make_response({"message": "Invalid postal code"}, 400)
    if not validate_nric(nric):
        return make_response({"message": "Invalid NRIC"}, 400)
    duplicate_phone = users.find_one({"phone": phone})
    if duplicate_phone and duplicate_phone["session_token"] != session_token:
        return make_response(
            {"message": "User with that phone number already exists"}, 400
        )
    duplicate_email = users.find_one({"email": email})
    if duplicate_email and duplicate_email["session_token"] != session_token:
        return make_response(
            {"message": "User with that email address already exists"}, 400
        )
    users.update_one(
        {"session_token": session_token},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "gender": gender,
                "nric": str.upper(nric),
                "address1": address1,
                "address2": address2,
                "address3": address3 or None,
                "address4": address4,
            }
        },
    )
    return make_response({"message": "User updated successfully"}, 200)
