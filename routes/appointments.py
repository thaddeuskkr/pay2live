from flask import render_template
from app import app


@app.route("/appointments")
def about():
    return render_template("appointments.html", current_page="appointments")
