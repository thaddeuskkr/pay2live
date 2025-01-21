from flask import render_template, request, redirect
from app import app, users


@app.route("/register")
def register():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    if user.get("registered"):
        return redirect("/profile")
    return render_template("register.html", current_page="register", user=user)
