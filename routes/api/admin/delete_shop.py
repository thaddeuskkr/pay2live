from bson import ObjectId
from flask import request, make_response
from app import app, users, shop, carts


@app.route("/api/admin/shop/delete", methods=["DELETE"])
def a_delete_shop():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if not user["admin"]:
        return make_response({"message": "Unauthorized"})
    data = request.get_json()
    required_fields = ["id"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    id: str = data.get("id")

    item_to_delete = shop.find_one({"_id": ObjectId(id)})
    if not item_to_delete:
        return make_response({"message": "Item not found"}, 404)

    shop.delete_one({"_id": ObjectId(item_to_delete["_id"])})

    carts.update_many({}, {"$pull": {"items": {"id": ObjectId(item_to_delete["_id"])}}})

    return make_response({"message": "Item deleted successfully"}, 200)
