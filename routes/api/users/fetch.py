from flask import request, make_response
from app import app, users


@app.route("/api/users/fetch", methods=["GET"])
def fetch_user():
    session_token = request.cookies.get("session_token")
    user = (
        users.find_one({"session_token": session_token}, {"_id": False})
        if session_token
        else None
    )
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    return make_response(
        {"message": "Successfully retrieved user information", "user": user}, 200
    )
