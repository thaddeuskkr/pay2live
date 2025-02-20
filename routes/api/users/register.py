import re
from flask import request, make_response
from app import app, users
from util import validate_nric


@app.route("/api/users/register", methods=["POST"])
def register_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    required_fields = [
        "first_name",
        "last_name",
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
    email: str = data.get("email")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    address1: str = data.get("address1")
    address2: str = data.get("address2")
    address3: str = data.get("address3")
    address4: str = data.get("address4")
    if (
        len(first_name) < 1
        or len(last_name) < 1
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
    if not re.match(r"^\d{6}$", address4):
        return make_response({"message": "Invalid postal code"}, 400)
    if not validate_nric(nric):
        return make_response({"message": "Invalid NRIC"}, 400)
    if user and user["registered"] == True:
        return make_response(
            {"message": "User with that phone number is already registered"}, 400
        )
    if users.find_one({"email": email}):
        return make_response(
            {"message": "User with that email address is already registered"}, 400
        )
    users.update_one(
        {"session_token": session_token},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "gender": gender,
                "nric": str.upper(nric),
                "role": "patient",
                "address1": address1,
                "address2": address2,
                "address3": address3 or None,
                "address4": address4,
                "registered": True,
            }
        },
    )
    return make_response({"message": "User registered successfully"}, 200)
