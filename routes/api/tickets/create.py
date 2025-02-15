from typing import Any
from bson import ObjectId
from flask import request, make_response
import requests
from app import app, users, tickets, whatsapp_api_auth, whatsapp_api_url
from util import send_email


@app.route("/api/tickets/create", methods=["POST"])
def create_ticket():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    required_fields = ["name", "contact_method", "subject", "message"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    name: str = data.get("name")
    contact_method: str = data.get("contact_method")
    subject: str = data.get("subject")
    message: str = data.get("message")
    email: str = data.get("email")
    phone: str = data.get("phone")
    if contact_method == "email" and not email:
        return make_response({"message": "Missing email"}, 400)
    if contact_method == "phone" and not phone:
        return make_response({"message": "Missing phone number"}, 400)

    ticket: dict[str, Any] = {
        "name": name,
        "email": email if contact_method == "email" else None,
        "phone": phone if contact_method == "phone" else None,
        "subject": subject,
        "message": message,
        "status": "open",
        "user": ObjectId(user["_id"]) if user else None,
    }

    inserted = tickets.insert_one(ticket)

    if contact_method == "phone":
        request_response = requests.post(
            f"{whatsapp_api_url}",
            json={
                "to": f"65{user["phone"]}",
                "from": "pay2live",
                "message": f"*Your support ticket on pay2live has been created.\nYour ticket ID is *{str(inserted.inserted_id)}*.\n\nWe will get back to you as soon as possible.",
            },
            headers={"Authorization": whatsapp_api_auth},
        )
        if request_response.status_code != 200:
            return make_response(
                {
                    "message": f"Your ticket has been created, but there was an error sending a receipt. Your ticket ID is {inserted.inserted_id}."
                },
                500,
            )
        else:
            return make_response(
                {
                    "message": "Successfully created ticket",
                    "id": str(inserted.inserted_id),
                }
            )
    else:
        response = send_email(
            email,
            f"[pay2live] Support Ticket (ID: {str(inserted.inserted_id)})",
            f"Your support ticket on pay2live has been created.\nYour ticket ID is {str(inserted.inserted_id)}.\n\nWe will get back to you as soon as possible.",
        )
        if response["error"] is False:
            return make_response(
                {
                    "message": "Successfully created ticket",
                    "id": str(inserted.inserted_id),
                }
            )
        else:
            return make_response(
                {
                    "message": f"Your ticket has been created, but there was an error sending a receipt. Your ticket ID is {inserted.inserted_id}.",
                    "error": response["message"],
                },
                500,
            )
