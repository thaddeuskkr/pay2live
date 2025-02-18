from flask import render_template, redirect, request
from app import app, users


@app.route("/profile")
def profile():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    if not user["registered"]:
        return redirect("/register")
    return render_template("profile.html", current_page="profile", user=user)
