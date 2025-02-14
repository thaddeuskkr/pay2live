from bson import ObjectId
import requests
import os
from flask import request, make_response
from app import app, ready, users, queue
from config import abbreviations


@app.route("/api/queue/delete", methods=["DELETE"])
def delete_queue():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if user["role"] != "doctor":
        return make_response({"message": "Unauthorized"}, 403)
    data = request.get_json()
    if not ready:
        response = make_response(
            {
                "message": "Service is not ready. Please try again later.",
            },
            500,
        )
        return response
    required_fields = ["queue"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    queue_number: str = data.get("queue")
    dictionary = queue.find_one({"number": int(queue_number)})
    if not dictionary:
        return make_response({"message": "Queue number not found"}, 404)
    called_user = users.find_one({"_id": ObjectId(dictionary["user"])})
    if not called_user:
        return make_response({"message": "User not found"}, 404)
    queue.delete_one({"_id": ObjectId(dictionary["_id"])})
    request_response = requests.post(
        f"{os.environ["WHATSAPP_API_URL"]}",
        json={
            "to": f"65{called_user["phone"]}",
            "from": "pay2live",
            "message": f"{called_user["first_name"]} {called_user["last_name"]},\nYour queue number *{abbreviations[dictionary["service"]]}{str(dictionary['number']).rjust(3, "0")}* has been cancelled.",
        },
        headers={"Authorization": os.environ["OTP_TOKEN"]},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "message": "Successfully deleted service",
                "number": abbreviations[dictionary["service"]]
                + str(dictionary["number"]).rjust(3, "0"),
                "user": called_user["phone"],
            },
            200,
        )
    else:
        response = make_response(
            {
                "phone": called_user["phone"],
                "message": "Failed to send notification. Please try again later.",
            },
            500,
        )
    return response
