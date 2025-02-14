import os
import secrets
from flask import request, make_response
import requests
from app import app, users


@app.route("/api/users/deactivate", methods=["POST"])
def deactivate_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    otp: str = data.get("otp")

    if not otp or len(otp) != 6:
        otp = str(secrets.randbelow(10**6)).rjust(6, "0")
        request_response = requests.post(
            "https://develop.tkkr.dev/message",
            json={
                "to": f"65{user["phone"]}",
                "from": "pay2live",
                "message": f"*{otp}* is your one-time password to deactivate your *pay2live* account. Do note, once your account is deactivated, you will have to contact support to reactivate it. Do not share this OTP with anyone.",
            },
            headers={"Authorization": os.environ["OTP_TOKEN"]},
        )
        users.update_one({"session_token": session_token}, {"$set": {"otp2": otp}})
        if request_response.status_code == 200:
            response = make_response(
                {
                    "phone": user["phone"],
                    "message": f'An OTP has been sent to {user["phone"]} for verification. Enter the OTP and click "Apply Changes" to continue.',
                },
                418,
            )
            return response
        else:
            response = make_response(
                {
                    "phone": user["phone"],
                    "message": f"Failed to send OTP to {user["phone"]}. Please try again later.",
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

    update_result = users.update_one(
        {"session_token": session_token}, {"$set": {"active": False}}
    )
    if update_result.modified_count == 0:
        response = make_response(
            {
                "message": "Invalid session token",
            },
            401,
        )
        return response
    else:
        return make_response(
            {
                "message": "Successfully deactivated user account",
            },
            200,
        )
