from typing import Any
import requests
import os
import pymongo
from flask import request, make_response
from app import app, ready, users, queue
from config import abbreviations
import html

@app.route("/api/queue/get", methods=["POST"])
def get_queue():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    required_fields = ["service"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    if not ready:
        response = make_response(
            {
                "message": "Service is not ready. Please try again later.",
            },
            500,
        )
        return response
    service = data.get("service")
    if service not in abbreviations.keys():
        return make_response({"message": "Invalid service"}, 400)
    previous = queue.find_one(sort=[("_id", pymongo.DESCENDING)])
    dictionary: dict[str, Any] = {
        "service": service,
        "number": previous["number"] + 1 if previous else 1,
        "room": None,
        "user": user["_id"],
        "status": "waiting",
    }
    queue.insert_one(dictionary)
    request_response = requests.post(
        "https://develop.tkkr.dev/message",
        json={
            "to": f"65{user["phone"]}",
            "from": "pay2live",
            "message": f"*{abbreviations[dictionary["service"]]}{str(dictionary['number']).rjust(3, "0")}* is your queue number.",
        },
        headers={"Authorization": os.environ["OTP_TOKEN"]},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "message": "Successfully added to queue",
                "number": html.escape(abbreviations[dictionary["service"]])
                + str(dictionary["number"]).rjust(3, "0"),
                "user": user["phone"],
                "status": dictionary["status"],
            },
            200,
        )
    else:
        response = make_response(
            {
                "phone": user["phone"],
                "message": "Failed to send notification. Please try again later.",
            },
            500,
        )
    return response
