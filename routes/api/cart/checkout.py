import os
from bson import ObjectId
from flask import request, make_response
import requests
from app import app, users, orders
from util import luhn_check
from datetime import datetime
import re
import html

@app.route("/api/cart/checkout", methods=["POST"])
def checkout():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    data = request.get_json()
    required_fields = [
        "order",
        "firstName",
        "lastName",
        "email",
        "phone",
        "address1",
        "address2",
        "address4",
        "nameOnCard",
        "cardNumber",
        "cardExpiry",
        "cardCVV",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    order_id: str = data.get("order")
    first_name: str = data.get("firstName")
    last_name: str = data.get("lastName")
    email: str = data.get("email")
    phone: str = data.get("phone")
    address1: str = data.get("address1")
    address2: str = data.get("address2")
    address3: str = data.get("address3")
    address4: str = data.get("address4")
    name_on_card: str = data.get("nameOnCard")
    card_number: str = data.get("cardNumber")
    card_expiry: str = data.get("cardExpiry")
    card_cvv: str = data.get("cardCVV")
    order = orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        return make_response({"message": "Invalid order"}, 400)
    if str(order["user"]) != str(user["_id"]):
        return make_response({"message": "Order not owned by current user"}, 400)
    if order["paid"]:
        return make_response({"message": "Order has already been paid for"}, 400)
    if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return make_response({"message": "Invalid email address"}, 400)
    if not re.match(r"^\d{8}$", phone):
        return make_response({"message": "Invalid phone number"}, 400)
    if not luhn_check(card_number):
        return make_response({"message": "Invalid credit/debit card number"}, 400)
    try:
        card_expiry_date = datetime.strptime(card_expiry, "%m/%y")
        current_date = datetime.now()
        if card_expiry_date < current_date:
            return make_response(
                {
                    "message": "Card is either expired or expires soon. Please use a different card."
                },
                400,
            )
    except ValueError:
        return make_response(
            {"message": "Invalid card expiry date format (MM/YY)"}, 400
        )

    orders.update_one(
        {"_id": ObjectId(order_id)},
        {
            "$set": {
                "paid": True,
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
                "payment": {
                    "name": name_on_card,
                    "card_number": card_number,
                    "card_expiry": card_expiry,
                    "card_cvv": card_cvv,
                },
            }
        },
    )

    order_info = "\n".join(
        [
            f"- {item["info"]['name']} x {item['quantity']} (${item["info"]['price'] * item['quantity']})"
            for item in order["items"]
        ]
    )

    request_response = requests.post(
        "https://develop.tkkr.dev/message",
        json={
            "to": f"65{user["phone"]}",
            "from": "pay2live",
            "message": f"*_Your order has been confirmed._*\n*Order ID:* `{order_id}`\n\n*Your order:*\n{order_info}\n\n*Subtotal:* ${order["total"]:.2f}\n\n*Ship to:*\n{first_name} {last_name}\n{address1}\n{address2}{f"\n{address3}" if address3 else ""}\nSingapore {address4}\n\n*Payment:* Card ending with {card_number[-4:]}",
        },
        headers={"Authorization": os.environ["OTP_TOKEN"]},
    )

    print(request_response)

    return make_response(
        {"message": "Payment successful", "order_id": html.escape(str(order_id))}, 200
    )
