from typing import Any
from flask import render_template, request, redirect, flash
from app import app, appointments, users
from bson.objectid import ObjectId


@app.route("/appointments", methods=["GET", "POST"])
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

    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]

        new_appointment: dict[str, Any] = {
            "user": ObjectId(user["_id"]),
            "date": date,
            "time": time,
        }

        # Insert the appointment into MongoDB
        appointments.insert_one(new_appointment)

        flash("An appointment has been added successfully!", "success")
        return redirect("/appointments")

    appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))
    return render_template(
        "appointments.html", current_page="appointments", appointments=appointments_list
    )


@app.route("/appointments/edit/<appointment_id>", methods=["GET", "POST"])
def edit_appointment(appointment_id: str):
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

    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]

        # Update the appointment in MongoDB
        appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"date": date, "time": time}},
        )

        flash("An appointment has been updated successfully!", "success")
        return redirect("/appointments")

    # Fetch the appointment to be edited
    appointment = appointments.find_one({"_id": ObjectId(appointment_id)})

    return render_template("edit_appointment.html", appointment=appointment)


@app.route("/appointments/delete/<appointment_id>", methods=["POST"])
def delete_appointment(appointment_id: str):
    # Delete the appointment from MongoDB
    result = appointments.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count > 0:
        flash("An appointment has been deleted successfully!", "success")
    else:
        flash("Appointment not found.", "danger")
    return redirect("/appointments")
