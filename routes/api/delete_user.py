from flask import request, make_response
from app import app, users


@app.route("/api/delete_user", methods=["DELETE"])
def delete_user():
    if "session_token" in request.cookies:
        if len(request.cookies["session_token"]) > 5:
            auth = request.cookies["session_token"]
        else:
            response = make_response(
                {
                    "message": "Invalid session token",
                },
                401,
            )
            return response
    else:
        response = make_response(
            {
                "message": "No session token found",
            },
            401,
        )
        return response
    delete_result = users.delete_one({"session_token": auth})
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
