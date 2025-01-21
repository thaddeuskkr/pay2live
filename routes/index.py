from flask import render_template, request
from app import app, users


@app.route("/")
def index():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    return render_template("index.html", current_page="home", user=user)
