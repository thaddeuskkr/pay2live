from flask import render_template
from app import app


@app.route("/profile")
def profile():
    return render_template("profile.html", current_page="profile")
