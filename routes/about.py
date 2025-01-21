from flask import render_template, request
from app import app, users


@app.route("/about")
def about():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    return render_template("about.html", current_page="about", user=user)
