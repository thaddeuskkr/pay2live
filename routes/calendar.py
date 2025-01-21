from flask import render_template, redirect, request
from app import app, users


@app.route("/calendar")
def calendar():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    return render_template("calendar.html", current_page="calendar", user=user)
