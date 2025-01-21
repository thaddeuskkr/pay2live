from flask import request, make_response
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/edit/<appointment_id>", methods=["POST"])
def edit_appointment(appointment_id: str):
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

    # Update the appointment in MongoDB
    appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": {"date": date, "time": time}},
    )

    return make_response({"message": "Appointment updated successfully"}, 200)
