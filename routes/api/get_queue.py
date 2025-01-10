import requests
import os
import pymongo
from flask import request, make_response
from app import app, ready, users, queue


@app.route("/api/get_queue", methods=["POST"])
def get_queue():
    data = request.get_json()
    if not ready:
        response = make_response(
            {
                "message": "Service is not ready. Please try again later.",
            },
            500,
        )
        return response
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
    user = users.find_one({"session_token": auth})
    if user is None:
        response = make_response(
            {
                "message": "Invalid session token",
            },
            401,
        )
        return response
    else:
        required_fields = ["type"]
        missing_keys = set(required_fields - data.keys())
        if missing_keys:
            return make_response(
                {"error": f"Missing required fields: {missing_keys}"}, 400
            )
        type = data.get("type")
        if type not in ["A", "B", "C"]:
            response = make_response(
                {
                    "message": "Invalid queue type",
                },
                400,
            )
            return response
        previous = queue.find_one({"type": type}, sort=[("_id", pymongo.DESCENDING)])
        dictionary: dict[str, str | int] = {
            "type": type,
            "number": previous["number"] + 1 if previous is not None else 1,
            "user": user["_id"],
            "status": "waiting",
        }
        queue.insert_one(dictionary)
        response = make_response(
            {
                "message": "Successfully added to queue",
                "number": str(dictionary["type"]) + str(dictionary["number"]),
                "user": user["phone"],
                "status": dictionary["status"],
            },
            200,
        )
        request_response = requests.post(
            "https://develop.tkkr.dev/message",
            json={
                "to": f"65{user["phone"]}",
                "from": "pay2live",
                "message": f"*{dictionary['type']}{str(dictionary['number']).rjust(3, "0")}* is your queue number.",
            },
            headers={"Authorization": os.environ["OTP_TOKEN"]},
        )
        if request_response.status_code == 200:
            response = make_response(
                {
                    "phone": user["phone"],
                    "message": f"Queue number sent to {user['phone']}",
                },
                200,
            )
            return response
        else:
            response = make_response(
                {
                    "phone": user["phone"],
                    "message": "Failed to send OTP. Please try again later.",
                },
                500,
            )
        return response
