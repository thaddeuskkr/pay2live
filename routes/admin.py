from flask import render_template, redirect, request
from app import app, users


@app.route("/admin")
def admin():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return redirect("/login")
    if not user["admin"]:
        return redirect("/")
    return render_template("admin.html", current_page="admin", user=user)
