from flask import request, make_response
from app import app, logins


@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()
    if [
        "first_name",
        "last_name",
        "email",
        "phone",
        "gender",
        "nric",
        "admin",
        "role",
        "address",
    ] not in data:
        return make_response({"error": "Missing required fields"}, 400)
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    email: str = data.get("email")
    phone: str = data.get("phone")
    gender: str = data.get("gender")
    nric: str = data.get("nric")
    role: str = data.get("role")
    address: str = data.get("address")
    login = logins.find_one({"phone": phone})
    if (
        len(first_name) < 1
        or len(last_name) < 1
        or len(email) < 1
        or len(phone) < 1
        or len(gender) <= 0
        or len(nric) < 1
        or len(role) < 1
        or len(address) < 1
    ):
        return make_response({"error": "Invalid text in input fields"}, 400)
