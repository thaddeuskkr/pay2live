import time
from typing import Any
from bson import ObjectId
from flask import request, make_response
from app import app, appointments, users, services


@app.route("/api/appointments/add", methods=["POST"])
def add_appointment():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    data = request.get_json()
    required_fields = ["timestamp", "service"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    service: str = data.get("service")
    timestamp: str = data.get("timestamp")
    patient_id: str = data.get("patient")

    current_time_ms = int(time.time() * 1000)

    if service not in services.keys():
        return make_response({"message": "Invalid service"}, 400)

    if int(timestamp) < current_time_ms:
        return make_response({"message": "Cannot book an appointment in the past"}, 400)

    if user["role"] == "doctor":
        if not patient_id:
            return make_response(
                {"message": f'Missing required fields: "patient"'}, 400
            )
        patient = users.find_one({"_id": ObjectId(patient_id)})
        if not patient:
            return make_response({"message": "Invalid patient ID"}, 400)
        new_appointment: dict[str, Any] = {
            "user": ObjectId(patient["_id"]),
            "service": service,
            "timestamp": timestamp,
            "doctor": ObjectId(user["_id"]),
        }
    else:
        new_appointment: dict[str, Any] = {
            "user": ObjectId(user["_id"]),
            "service": service,
            "timestamp": timestamp,
            "doctor": None,
        }

    # Insert the appointment into MongoDB
    appointments.insert_one(new_appointment)

    return make_response({"message": "Appointment added successfully"}, 200)
