from zoneinfo import ZoneInfo
from flask import render_template, request, redirect
from app import app, appointments, users
from bson.objectid import ObjectId
from datetime import datetime

services = {
    "consultation": "Consultation",
    "collection": "Medicine Collection",
    "blood": "Blood Test",
    "dental": "Dental Checkup",
    "eye-exam": "Eye Examination",
    "vaccination": "Vaccination",
}


@app.route("/appointments", methods=["GET"])
def appointments_route():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")

    if user["role"] == "admin":
        appointments_list = list(appointments.find())
    elif user["role"] == "doctor":
        appointments_list = list(appointments.find({"doctor": ObjectId(user["_id"])}))
    else:
        appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))

    for appointment in appointments_list:
        appointment["raw"] = appointment
        datetime_object = datetime.fromtimestamp(
            int(appointment["timestamp"]) / 1000, tz=ZoneInfo("Asia/Singapore")
        )
        appointment["service"] = services[appointment["service"]]
        appointment["doctor"] = users.find_one({"_id": appointment["doctor"]})
        appointment["user"] = users.find_one({"_id": appointment["user"]})
        appointment["date"] = datetime_object.strftime(
            "%d/%m/%Y",
        )
        appointment["time"] = datetime_object.strftime("%I:%M %p")
        appointment["id"] = str(appointment["_id"])

    services_list: list[dict[str, str]] = []
    for service in services.keys():
        services_list.append({"id": service, "name": services[service]})

    return render_template(
        "appointments.html",
        current_page="appointments",
        appointments=sorted(appointments_list, key=lambda x: x["timestamp"]),
        doctors=users.find({"role": "doctor"}),
        services=services_list,
        user=user,
    )
