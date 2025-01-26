from zoneinfo import ZoneInfo
from flask import render_template, request, redirect
from app import app, appointments, users
from config import services
from bson.objectid import ObjectId
from datetime import datetime
import time


@app.route("/appointments", methods=["GET"])
def appointments_route():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")

    filter = request.args.get("filter", "upcoming")

    if filter == "new":
        if user["role"] != "doctor":
            return redirect("/appointments")
        appointments_list = [
            x
            for x in appointments.find({"doctor": None})
            if (x["timestamp"] + 3_600_000) >= (time.time() * 1000)
        ]
        filter_header = "Unclaimed Appointments"
    elif filter == "past":
        if user["role"] == "admin":
            appointments_list = list(appointments.find())
        elif user["role"] == "doctor":
            appointments_list = list(
                appointments.find({"doctor": ObjectId(user["_id"])})
            )
        else:
            appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))
        appointments_list = [
            x
            for x in appointments_list
            if (x["timestamp"] + 3_600_000) <= (time.time() * 1000)
        ]
        filter_header = "Past Appointments"
    else:
        if user["role"] == "admin":
            appointments_list = list(appointments.find())
        elif user["role"] == "doctor":
            appointments_list = list(
                appointments.find({"doctor": ObjectId(user["_id"])})
            )
        else:
            appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))
        filter_header = "Upcoming Appointments"
        appointments_list = [
            x
            for x in appointments_list
            if (x["timestamp"] + 3_600_000) >= (time.time() * 1000)
        ]

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
        filter_header=filter_header,
        current_page="appointments",
        appointments=sorted(appointments_list, key=lambda x: x["timestamp"]),
        doctors=users.find({"role": "doctor"}),
        patients=users.find({"role": "patient"}),
        services=services_list,
        user=user,
    )
