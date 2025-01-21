from flask import make_response, request
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/delete", methods=["DELETE"])
def delete_appointment():
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
    required_fields = ["id"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response({"error": f"Missing required fields: {missing_keys}"}, 400)
    appointment_id: str = data.get("id")
    # Delete the appointment from MongoDB
    appointment = appointments.find_one({"_id": ObjectId(appointment_id)})
    if appointment is None:
        response = make_response({"message": "Appointment not found"}, 404)
        return response
    if (
        appointment["user"] != user["_id"]
        and appointment["doctor"] != user["_id"]
        and not user["admin"]
    ):
        response = make_response(
            {"message": "You do not have permission to delete this appointment"}, 403
        )
        return response
    result = appointments.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count > 0:
        response = make_response({"message": "Appointment deleted successfully"}, 200)
        return response
    else:
        response = make_response({"message": "Appointment not found"}, 404)
        return response
