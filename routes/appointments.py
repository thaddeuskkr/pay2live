from flask import render_template
from app import app


@app.route("/appointments")
def appointments():
    return render_template("appointments.html", current_page="appointments")
