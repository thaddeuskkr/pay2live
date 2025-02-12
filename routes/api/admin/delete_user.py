from bson import ObjectId
from flask import request, make_response
from app import app, users


@app.route("/api/admin/users/delete", methods=["DELETE"])
def a_delete_user():
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
    user_to_delete = users.find_one({"_id": ObjectId(id)})
    if not user_to_delete:
        return make_response({"message": "User not found"}, 404)
    users.delete_one(
        {"_id": ObjectId(user_to_delete["_id"])},
    )
    return make_response({"message": "User deleted successfully"}, 200)
