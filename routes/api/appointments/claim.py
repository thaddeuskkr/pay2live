from flask import request, make_response
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/claim", methods=["POST"])
def claim_appointment():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)

    data = request.get_json()
    required_fields = ["id"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    id: str = data.get("id")

    if user["role"] != "doctor":
        return make_response({"message": "Only doctors can claim appointments"}, 403)

    appointment = appointments.find_one({"_id": ObjectId(id)})
    if not appointment:
        return make_response({"message": "Invalid appointment ID"}, 400)

    if appointment["doctor"]:
        return make_response({"message": "Appointment already claimed"}, 400)

    # Update the appointment in MongoDB
    appointments.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"doctor": ObjectId(user["_id"])}},
    )

    return make_response({"message": "Appointment claimed successfully"}, 200)
