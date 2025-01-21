from flask import request, make_response
from app import app, users


@app.route("/api/users/register", methods=["POST"])
def register_user():
    data = request.get_json()
    required_fields = [
        "first_name",
        "last_name",
        "email",
        "gender",
        "nric",
        "role",
        "address",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response({"error": f"Missing required fields: {missing_keys}"}, 400)
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    email: str = data.get("email")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    role: str = data.get("role")
    address: str = data.get("address")
    if (
        len(first_name) < 1
        or len(last_name) < 1
        or len(email) < 1
        or len(gender) <= 0
        or len(nric) < 1
        or len(role) < 1
        or len(address) < 1
    ):
        return make_response({"error": "Invalid text in input fields"}, 400)
    if "session_token" in request.cookies:
        if len(request.cookies["session_token"]) > 5:
            auth = request.cookies["session_token"]
        else:
            response = make_response(
                {
                    "message": "Invalid session token",
                },
                401,
            )
            return response
    else:
        response = make_response(
            {
                "message": "No session token found",
            },
            401,
        )
        return response
    user = users.find_one({"session_token": auth})
    if user is None:
        response = make_response(
            {
                "message": "Invalid session token",
            },
            401,
        )
        return response
    if user and user["registered"] == True:
        return make_response(
            {"message": "User with that phone number is already registered"}, 400
        )
    if users.find_one({"email": email}):
        return make_response(
            {"message": "User with that email address is already registered"}, 400
        )
    users.update_one(
        {"session_token": auth},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "gender": gender,
                "nric": nric,
                "role": role,
                "address": address,
                "registered": True,
            }
        },
    )
    return make_response({"message": "User registered successfully"}, 200)
