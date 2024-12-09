from flask import render_template
from pay2live import app


@app.route("/")
def index():
    return render_template("index.html")
