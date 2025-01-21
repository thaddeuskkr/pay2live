from flask import render_template, request, redirect
from app import app, users


@app.route("/login")
def login():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if user is not None:
        return redirect("/profile")
    return render_template("login.html", current_page="login", user=user)
