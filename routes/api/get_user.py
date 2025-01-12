from flask import request, make_response
from app import app, users


@app.route("/api/get_user", methods=["GET"])
def get_user():
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
    user = users.find_one({"session_token": auth}, {"_id": False})
    if user is None:
        response = make_response(
            {
                "message": "Invalid session token",
            },
            401,
        )
        return response
    return make_response(
        {"message": "Successfully retrieved user information", "user": user}, 200
    )
