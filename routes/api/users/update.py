from flask import request, make_response
from app import app, users


@app.route("/api/users/update", methods=["POST"])
def update_user():
    data = request.get_json()
    required_fields = [
        "first_name",
        "last_name",
        "phone",
        "email",
        "gender",
        "nric",
        "address",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response({"error": f"Missing required fields: {missing_keys}"}, 400)
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    phone: str = data.get("phone")
    email: str = data.get("email")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    address: str = data.get("address")
    if (
        len(first_name) < 1
        or len(last_name) < 1
        or len(phone) < 1
        or len(email) < 1
        or len(gender) <= 0
        or len(nric) < 1
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
    duplicate_phone = users.find_one({"phone": phone})
    if duplicate_phone and duplicate_phone["session_token"] != auth:
        return make_response(
            {"message": "User with that phone number already exists"}, 400
        )
    duplicate_email = users.find_one({"email": email})
    if duplicate_email and duplicate_email["session_token"] != auth:
        return make_response(
            {"message": "User with that email address already exists"}, 400
        )
    users.update_one(
        {"session_token": auth},
        {
            "$set": {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": phone,
                "gender": gender,
                "nric": nric,
                "address": address,
            }
        },
    )
    return make_response({"message": "User updated successfully"}, 200)
