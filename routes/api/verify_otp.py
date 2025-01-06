import secrets
from flask import request, make_response
from app import app, logins


@app.route("/api/verify_otp", methods=["POST"])
def verify_otp():
    data = request.get_json()
    otp: str = data.get("otp")
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
    if (len(otp) != 6) or (not otp.isdigit()):
        response = make_response(
            {
                "phone": phone,
                "message": "Invalid OTP",
            },
            400,
        )
        return response
    login = logins.find_one({"phone": phone})
    if login is None:
        response = make_response(
            {
                "phone": phone,
                "message": "No OTP has been sent for this phone number",
            },
            400,
        )
        response.delete_cookie("session_token")
        return response
    elif login["otp"] == otp:
        try:
            if len(login["session_token"]) > 5:
                session_token = login["session_token"]
            else:
                session_token = secrets.token_urlsafe(64)
        except KeyError:
            session_token = secrets.token_urlsafe(64)
        logins.update_one(
            {"phone": phone}, {"$set": {"session_token": session_token, "otp": None}}
        )
        response = make_response(
            {
                "phone": phone,
                "session_token": session_token,
                "message": "OTP successfully verified",
            },
            200,
        )
        response.set_cookie(
            "session_token",
            value=session_token,
            max_age=None,
            expires=None,
            path="/",
            domain=None,
        )
        response.set_cookie(
            "phone",
            value=phone,
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
