from typing import Any
from bson import ObjectId
from flask import request, make_response
from app import app, appointments, users


@app.route("/api/appointments/add", methods=["POST"])
def add_appointment():
    if "session_token" in request.cookies:
        if len(request.cookies["session_token"]) > 5:
            auth = request.cookies["session_token"]
        else:
            response = make_response({"message": "Invalid session token"}, 401)
            return response
    else:
        response = make_response({"message": "No session token found"}, 401)
        return response
    user = users.find_one({"session_token": auth})
    if user is None:
        response = make_response({"message": "Invalid session token"}, 401)
        return response

    date = request.form["date"]
    time = request.form["time"]

    new_appointment: dict[str, Any] = {
        "user": ObjectId(user["_id"]),
        "date": date,
        "time": time,
    }

    # Insert the appointment into MongoDB
    appointments.insert_one(new_appointment)

    return make_response({"message": "Appointment added successfully"}, 200)
