from bson import ObjectId
import requests
import os
from flask import request, make_response
from app import app, ready, users, queue
from config import abbreviations


@app.route("/api/queue/call", methods=["POST"])
def call_queue():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if user["role"] != "doctor":
        return make_response({"message": "Unauthorized"}, 403)
    data = request.get_json()
    required_fields = ["room"]
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
    room: str = data.get("room")
    patient: str = data.get("patient")
    queue_number: str = data.get("queue")
    if not patient and not queue_number:
        return make_response(
            {"message": 'Missing either fields: "patient", "queue"'}, 400
        )
    previous_patient = queue.find_one({"room": int(room), "status": "current"})
    if previous_patient:
        previous_patient_user = users.find_one({"_id": previous_patient["user"]})
        if not previous_patient_user:
            return make_response({"message": "User not found"}, 404)
        request_response = requests.post(
            "https://develop.tkkr.dev/message",
            json={
                "to": f"65{previous_patient_user['phone']}",
                "from": "pay2live",
                "message": f"{previous_patient_user['first_name']} {previous_patient_user["last_name"]},\nYou have just missed your queue number *{abbreviations[previous_patient['service']]}{str(previous_patient['number']).rjust(3, '0')}*.\nPlease speak to the clinic staff if you require further assistance.",
            },
            headers={"Authorization": os.environ["OTP_TOKEN"]},
        )
        queue.update_one(
            {"_id": previous_patient["_id"]}, {"$set": {"status": "missed"}}
        )
    dictionary = None
    if patient:
        dictionary = queue.find_one({"user": ObjectId(patient)})
    if queue_number:
        dictionary = queue.find_one({"number": int(queue_number)})
    if not dictionary:
        return make_response({"message": "Queue number or patient not found"}, 404)
    if dictionary["status"] not in ["waiting", "missed"]:
        return make_response({"message": "Queue number already called"}, 400)
    called_user = users.find_one({"_id": dictionary["user"]})
    if not called_user:
        return make_response({"message": "User not found"}, 404)
    queue.update_one(
        {"_id": dictionary["_id"]}, {"$set": {"status": "current", "room": int(room)}}
    )
    request_response = requests.post(
        "https://develop.tkkr.dev/message",
        json={
            "to": f"65{called_user["phone"]}",
            "from": "pay2live",
            "message": f"{called_user["first_name"]} {called_user["last_name"]},\nYour queue number *{abbreviations[dictionary["service"]]}{str(dictionary['number']).rjust(3, "0")}* has been called.\nPlease proceed to room {room} immediately.",
        },
        headers={"Authorization": os.environ["OTP_TOKEN"]},
    )
    if request_response.status_code == 200:
        response = make_response(
            {
                "message": "Successfully called queue number",
                "number": abbreviations[dictionary["service"]]
                + str(dictionary["number"]).rjust(3, "0"),
                "user": called_user["phone"],
                "room": int(room),
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
