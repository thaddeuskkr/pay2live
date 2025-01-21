from flask import render_template, request, redirect
from app import app, appointments, users
from bson.objectid import ObjectId


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

    appointments_list = list(appointments.find({"user": ObjectId(user["_id"])}))
    return render_template(
        "appointments.html", current_page="appointments", appointments=appointments_list
    )
