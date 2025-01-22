import time
from flask import request, make_response
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/edit", methods=["POST"])
def edit_appointment():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    data = request.get_json()
    required_fields = ["timestamp", "id"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    id: str = data.get("id")
    timestamp: str = data.get("timestamp")

    current_time_ms = int(time.time() * 1000)

    if int(timestamp) < current_time_ms:
        return make_response({"message": "Cannot move an appointment to the past"}, 400)

    # Update the appointment in MongoDB
    appointments.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"timestamp": timestamp, "doctor": None}},
    )

    return make_response({"message": "Appointment edited successfully"}, 200)
