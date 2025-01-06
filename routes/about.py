from flask import render_template
from app import app


@app.route("/about")
def about():
    return render_template("about.html", current_page="about")
