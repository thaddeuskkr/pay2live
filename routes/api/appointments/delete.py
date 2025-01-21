from flask import make_response
from app import app, appointments
from bson.objectid import ObjectId


@app.route("/api/appointments/delete/<appointment_id>", methods=["POST"])
def delete_appointment(appointment_id: str):
    # Delete the appointment from MongoDB
    result = appointments.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count > 0:
        response = make_response({"message": "Appointment deleted successfully"}, 200)
        return response
    else:
        response = make_response({"message": "Appointment not found"}, 404)
        return response
