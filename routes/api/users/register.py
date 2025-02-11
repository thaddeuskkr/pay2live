from flask import request, make_response
from app import app, users


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
        "role",
        "address1",
        "address2",
        "address3",
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
    role: str = data.get("role")
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
        or len(role) < 1
        or len(address1) < 1
        or len(address2) < 1
        or len(address4) < 1
    ):
        return make_response({"message": "Invalid text in input fields"}, 400)
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
                "nric": nric,
                "role": role,
                "address1": address1,
                "address2": address2,
                "address3": address3 or None,
                "address4": address4,
                "registered": True,
            }
        },
    )
    return make_response({"message": "User registered successfully"}, 200)
