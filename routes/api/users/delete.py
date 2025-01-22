from flask import request, make_response
from app import app, users


@app.route("/api/users/delete", methods=["DELETE"])
def delete_user():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    delete_result = users.delete_one({"session_token": session_token})
    if delete_result.deleted_count == 0:
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
                "message": "Successfully deleted user information",
            },
            200,
        )
