from flask import request, make_response
from app import app, users


@app.route("/api/users/deactivate", methods=["DELETE"])
def deactivate_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    update_result = users.update_one(
        {"session_token": session_token}, {"$set": {"active": False}}
    )
    if update_result.modified_count == 0:
        response = make_response(
            {
                "message": "Invalid session token",
            },
            401,
        )
        return response
    else:
        return make_response(
            {
                "message": "Successfully deactivated user account",
            },
            200,
        )
