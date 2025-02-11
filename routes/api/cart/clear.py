from bson import ObjectId
from flask import request, make_response
from app import app, users, carts


@app.route("/api/cart/clear", methods=["POST"])
def clear_cart():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    carts.update_one(
        {"user": ObjectId(user["_id"])}, {"$set": {"items": []}}, upsert=True
    )

    return make_response({"message": "Items cleared from cart successfully"}, 200)
