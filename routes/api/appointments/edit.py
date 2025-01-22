from flask import request, make_response
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/edit", methods=["POST"])
def edit_appointment():
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

    data = request.get_json()
    required_fields = ["timestamp", "id"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response({"error": f"Missing required fields: {missing_keys}"}, 400)
    id: str = data.get("id")
    timestamp: str = data.get("timestamp")

    # Update the appointment in MongoDB
    appointments.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"timestamp": timestamp, "doctor": None}},
    )

    return make_response({"message": "Appointment updated successfully"}, 200)
