from bson import ObjectId
import requests
from flask import request, make_response
from app import app, ready, users, queue, otp_token, whatsapp_api_url
from config import abbreviations


@app.route("/api/queue/complete", methods=["POST"])
def complete_queue():
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
    room: str = data.get("room")
    patient: str = data.get("patient")
    queue_number: str = data.get("queue")
    if not patient and not queue_number and not room:
        return make_response(
            {"message": 'Missing either fields: "patient", "queue", "room"'}, 400
        )
    dictionary = None
    if patient:
        dictionary = queue.find_one({"user": ObjectId(patient)})
    if queue_number:
        dictionary = queue.find_one({"number": int(queue_number)})
    if room:
        dictionary = queue.find_one({"room": int(room), "status": "current"})
    if not dictionary:
        return make_response(
            {"message": "Queue number, room or patient not found"}, 404
        )
    if dictionary["status"] != "current":
        return make_response({"message": "Queue number not called"}, 400)
    called_user = users.find_one({"_id": ObjectId(dictionary["user"])})
    if not called_user:
        return make_response({"message": "User not found"}, 404)
    queue.update_one(
        {"_id": ObjectId(dictionary["_id"])}, {"$set": {"status": "completed"}}
    )
    request_response = requests.post(
        f"{whatsapp_api_url}",
        json={
            "to": f"65{called_user["phone"]}",
            "from": "pay2live",
            "message": f"{called_user["first_name"]} {called_user["last_name"]},\nThank you for visiting our clinic.",
        },
        headers={"Authorization": otp_token},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "message": "Successfully completed service",
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
