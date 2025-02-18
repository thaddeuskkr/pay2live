import re
from flask import request, make_response
from app import app, users
from util import validate_nric


@app.route("/api/admin/users/add", methods=["POST"])
def a_add_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if not user["admin"]:
        return make_response({"message": "Unauthorized"})
    data = request.get_json()
    required_fields = [
        "phone",
        "first_name",
        "last_name",
        "email",
        "gender",
        "nric",
        "role",
        "admin",
        "registered",
        "active",
        "address1",
        "address2",
        "address4",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    phone: str = data.get("phone")
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    email: str = data.get("email")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    role: str = data.get("role")
    admin: str = data.get("admin")
    registered: str = data.get("registered")
    active: str = data.get("active")
    address1: str = data.get("address1")
    address2: str = data.get("address2")
    address3: str = data.get("address3")
    address4: str = data.get("address4")

    if gender not in ["male", "female", "other"]:
        return make_response({"message": "Invalid gender"}, 400)
    if role not in ["patient", "doctor"]:
        return make_response({"message": "Invalid role"}, 400)
    if admin not in ["true", "false"]:
        return make_response({"message": "Invalid admin status"}, 400)
    if registered not in ["true", "false"]:
        return make_response({"message": "Invalid registered status"}, 400)
    if active not in ["true", "false"]:
        return make_response({"message": "Invalid active status"}, 400)
    if not re.match(r"^[a-zA-Z]+$", first_name):
        return make_response({"message": "Invalid first name"}, 400)
    if not re.match(r"^[a-zA-Z]+$", last_name):
        return make_response({"message": "Invalid last name"}, 400)
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return make_response({"message": "Invalid email address"}, 400)
    if not re.match(r"^\d{8}$", phone):
        return make_response({"message": "Invalid phone number"}, 400)
    if not validate_nric(nric):
        return make_response({"message": "Invalid NRIC"}, 400)
    duplicate_phone = users.find_one({"phone": phone})
    if duplicate_phone:
        return make_response(
            {"message": "User with that phone number already exists"}, 400
        )
    duplicate_email = users.find_one({"email": email})
    if duplicate_email:
        return make_response(
            {"message": "User with that email address already exists"}, 400
        )
    duplicate_nric = users.find_one({"nric": str.upper(nric)})
    if duplicate_nric:
        return make_response({"message": "User with that NRIC already exists"}, 400)

    users.insert_one(
        {
            "phone": phone,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "gender": gender,
            "nric": str.upper(nric),
            "role": role,
            "address1": address1,
            "address2": address2,
            "address3": address3,
            "address4": address4,
            "session_token": None,
            "otp": None,
            "otp2": None,
            "admin": admin == "true",
            "registered": registered == "true",
            "active": active == "true",
        }
    )
    return make_response({"message": "User updated successfully"}, 200)
