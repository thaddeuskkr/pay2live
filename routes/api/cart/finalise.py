from typing import Any
from bson import ObjectId
from flask import request, make_response
from app import app, users, carts, shop, orders


@app.route("/api/cart/finalise", methods=["POST"])
def finalise_cart():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    cart = carts.find_one({"user": ObjectId(user["_id"])}) if user else None
    if not cart:
        return make_response({"message": "No items in cart"}, 400)
    cart_items: list[dict[str, Any]] = []
    if cart:
        for item in cart["items"]:
            item_data = shop.find_one({"_id": ObjectId(item["id"])})
            cart_items.append(
                {
                    "info": item_data,
                    "quantity": item["quantity"],
                }
            )
    subtotal = 0.00
    for item in cart_items:
        subtotal += item["info"]["price"] * item["quantity"]

    order: dict[str, Any] = {
        "user": ObjectId(user["_id"]),
        "items": cart_items,
        "total": subtotal,
        "paid": False,
        "fulfilled": False,
        "payment": {
            "name": None,
            "card_number": None,
            "card_expiry": None,
            "card_cvv": None,
        },
        "shipping": {
            "first_name": None,
            "last_name": None,
            "email": None,
            "phone": None,
            "address1": None,
            "address2": None,
            "address3": None,
            "address4": None,
        },
    }

    result = orders.insert_one(order)
    carts.delete_one({"_id": ObjectId(cart["_id"])})

    return make_response(
        {
            "message": f"Order {result.inserted_id} finalised",
            "order_id": str(result.inserted_id),
        },
        200,
    )
