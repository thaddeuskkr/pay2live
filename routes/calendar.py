from flask import render_template, redirect, request
from app import app, users


@app.route("/calendar")
def calendar():
    if "session_token" in request.cookies:
        if len(request.cookies["session_token"]) > 5:
            auth = request.cookies["session_token"]
        else:
            return redirect("/login")
    else:
        return redirect("/login")
    user = users.find_one({"session_token": auth})
    if user is None:
        return redirect("/login")
    return render_template("calendar.html", current_page="calendar")
