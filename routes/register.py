from flask import render_template
from app import app


@app.route("/register")
def register():
    return render_template("register.html", current_page="register")
