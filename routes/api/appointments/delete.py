from flask import make_response, request
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/api/appointments/delete", methods=["DELETE"])
def delete_appointment():
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
    appointment_id: str = data.get("id")
    # Delete the appointment from MongoDB
    appointment = appointments.find_one({"_id": ObjectId(appointment_id)})
    if appointment is None:
        response = make_response({"message": "Appointment not found"}, 404)
        return response
    if (
        str(appointment["user"]) != str(user["_id"])
        and str(appointment["doctor"]) != str(user["_id"])
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
