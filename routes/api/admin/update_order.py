import re
from bson import ObjectId
from flask import request, make_response
from app import app, users, orders


@app.route("/api/admin/orders/update", methods=["POST"])
def a_update_order():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if not user["admin"]:
        return make_response({"message": "Unauthorized"})
    data = request.get_json()
    required_fields = ["id", "paid", "fulfilled"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    id: str = data.get("id")
    paid: str = data.get("paid")
    fulfilled: str = data.get("fulfilled")
    first_name: str = data.get("first_name")
    last_name: str = data.get("last_name")
    email: str = data.get("email")
    phone: str = data.get("phone")
    address1: str = data.get("address1")
    address2: str = data.get("address2")
    address3: str = data.get("address3")
    address4: str = data.get("address4")

    if paid not in ["true", "false"]:
        return make_response({"message": "Invalid paid status"}, 400)

    if fulfilled not in ["true", "false"]:
        return make_response({"message": "Invalid fulfilled status"}, 400)

    order = orders.find_one({"_id": ObjectId(id)})
    if not order:
        return make_response({"message": "Order not found"}, 404)

    if not re.match(r"^[a-zA-Z]+$", first_name):
        return make_response({"message": "Invalid first name"}, 400)
    if not re.match(r"^[a-zA-Z]+$", last_name):
        return make_response({"message": "Invalid last name"}, 400)
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return make_response({"message": "Invalid email address"}, 400)
    if not re.match(r"^\d{8}$", phone):
        return make_response({"message": "Invalid phone number"}, 400)
    if not re.match(r"^\d{6}$", address4):
        return make_response({"message": "Invalid postal code"}, 400)

    orders.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "paid": paid == "true",
                "fulfilled": fulfilled == "true",
                "shipping": {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "address1": address1,
                    "address2": address2,
                    "address3": address3 or None,
                    "address4": address4,
                },
            }
        },
    )

    return make_response({"message": "Order updated successfully"}, 200)
