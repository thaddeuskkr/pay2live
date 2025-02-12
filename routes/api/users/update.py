from flask import request, make_response
from app import app, users
from util import validate_nric


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
