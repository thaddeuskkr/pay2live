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
    if "session_token" in request.cookies:
        if len(request.cookies["session_token"]) > 5:
            auth = request.cookies["session_token"]
        else:
            return redirect("/login")
    else:
        return redirect("/login")
    user = users.find_one({"session_token": auth})
    if user is None:
        return redirect("/login")

    if user["role"] == "admin":
        appointments_list = list(appointments.find())
    elif user["role"] == "doctor":
        appointments_list = list(appointments.find({"doctor": ObjectId(user["_id"])}))
    else:
        appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))

    for appointment in appointments_list:
        datetime_object = datetime.fromtimestamp(int(appointment["timestamp"]) / 1000)
        appointment["service"] = services[appointment["service"]]
        appointment["doctor"] = users.find_one({"_id": appointment["doctor"]})
        appointment["user"] = users.find_one({"_id": appointment["user"]})
        appointment["date"] = datetime_object.strftime("%Y-%m-%d")
        appointment["time"] = datetime_object.strftime("%H:%M:%S")
        appointment["id"] = str(appointment["_id"])

    services_list: list[dict[str, str]] = []
    for service in services.keys():
        services_list.append({"id": service, "name": services[service]})

    return render_template(
        "appointments.html",
        current_page="appointments",
        appointments=appointments_list,
        doctors=users.find({"role": "doctor"}),
        services=services_list,
    )
