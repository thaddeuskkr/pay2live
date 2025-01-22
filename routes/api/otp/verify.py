import secrets
from flask import request, make_response
from app import app, users
import html


@app.route("/api/otp/verify", methods=["POST"])
def verify_otp():
    data = request.get_json()
    required_fields = ["otp", "phone"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    otp: str = data.get("otp")
    phone: str = html.escape(data.get("phone"))
    if (len(phone) != 8) or (not phone.isdigit()):
        response = make_response(
            {
                "phone": phone,
                "message": "Invalid phone number",
            },
            400,
        )
        return response
    if (len(otp) != 6) or (not otp.isdigit()):
        response = make_response(
            {
                "phone": phone,
                "message": "Invalid OTP",
            },
            400,
        )
        return response
    user = users.find_one({"phone": phone})
    if user is None:
        response = make_response(
            {
                "phone": phone,
                "message": "No OTP has been sent for this phone number",
            },
            400,
        )
        response.delete_cookie("session_token")
        return response
    elif user["otp"] is None:
        response = make_response(
            {
                "phone": phone,
                "message": "No OTP has been sent for this phone number",
            },
            400,
        )
        response.delete_cookie("session_token")
        return response
    elif user["otp"] == otp:
        try:
            if len(user["session_token"] or "") > 5:
                session_token = user["session_token"]
            else:
                session_token = secrets.token_urlsafe(64)
        except KeyError:
            session_token = secrets.token_urlsafe(64)
        users.update_one(
            {"phone": phone}, {"$set": {"session_token": session_token, "otp": None}}
        )
        response = make_response(
            {
                "phone": phone,
                "session_token": session_token,
                "message": "OTP successfully verified",
                "registered": user["registered"],
            },
            200,
        )
        response.set_cookie(
            "session_token",
            httponly=True,
            secure=True,
            samesite="Lax",
            value=session_token,
            max_age=None,
            expires=None,
            path="/",
            domain=None,
        )
        return response
    else:
        response = make_response(
            {
                "phone": phone,
                "message": "Invalid OTP",
            },
            400,
        )
        response.delete_cookie("session_token")
        return response
