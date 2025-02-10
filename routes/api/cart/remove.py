from typing import Any
from bson import ObjectId
from flask import request, make_response
from app import app, users, carts, shop


@app.route("/api/cart/remove", methods=["POST"])
def remove_cart():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    data = request.get_json()
    required_fields = ["item", "quantity"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    item: str = data.get("item")
    quantity: str | int = data.get("quantity")

    if ObjectId(item) not in [item["_id"] for item in shop.find()]:
        return make_response({"message": "Item not found"}, 404)

    try:
        quantity = int(quantity)
    except ValueError:
        return make_response({"message": "Quantity must be a number"}, 400)

    cart: dict[str, Any] | None = carts.find_one({"user": ObjectId(user["_id"])})

    if not cart:
        cart = {"user": ObjectId(user["_id"]), "items": []}

    for cart_item in cart["items"]:
        if cart_item["id"] == ObjectId(item):
            cart_item["quantity"] -= int(quantity)
            if cart_item["quantity"] == 0:
                cart["items"].remove(cart_item)
            break
    else:
        return make_response({"message": "Item not in cart"}, 400)

    carts.update_one(
        {"user": ObjectId(user["_id"])}, {"$set": {"items": cart["items"]}}, upsert=True
    )

    return make_response({"message": "Item removed from cart successfully"}, 200)
