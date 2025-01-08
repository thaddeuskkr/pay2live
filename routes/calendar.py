from flask import render_template
from app import app


@app.route("/calendar")
def calendar():
    return render_template("calendar.html", current_page="calendar")
