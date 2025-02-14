from flask import make_response, request, redirect
from app import app, users, debug


@app.route("/logout")
def logout():
    reset_token = (
        request.args.get("reset_token", "false") == "true"
        or request.args.get("reset_token", "0") == "1"
    )
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if user is not None:
        if reset_token:
            users.update_one(
                {"session_token": session_token},
                {"$set": {"session_token": None}},
            )
    response = make_response(redirect("/"))
    response.set_cookie(
        "session_token",
        httponly=True,
        secure=(debug == False),
        samesite="Lax",
        value="",
        max_age=None,
        expires=None,
        path="/",
        domain=None,
    )
    return response
