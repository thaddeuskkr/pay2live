from util import send_email
from bson import ObjectId
from flask import request, make_response
import requests
from app import app, users, tickets, whatsapp_api_auth, whatsapp_api_url
from util import send_email


@app.route("/api/tickets/respond", methods=["POST"])
def respond_ticket():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    data = request.get_json()
    required_fields = ["id", "response"]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    id: str = data.get("id")
    response: str = data.get("response")

    ticket = tickets.find_one({"_id": ObjectId(id)})
    if not ticket:
        return make_response({"message": "Ticket not found"}, 404)

    tickets.update_one(
        {"_id": ObjectId(id)},
        {"$set": {"response": response, "status": "closed"}},
    )

    if ticket["phone"]:
        request_response = requests.post(
            f"{whatsapp_api_url}",
            json={
                "to": f"65{ticket["phone"]}",
                "from": "pay2live",
                "message": f"*Your support ticket on pay2live has received a response.*\n*Ticket ID:* {str(ticket["_id"])}\n*Response:*\n{response}",
            },
            headers={"Authorization": whatsapp_api_auth},
        )
        if request_response.status_code != 200:
            return make_response(
                {
                    "message": f"Failed to respond to ticket as there was an error sending a WhatsApp message.",
                },
                500,
            )
        else:
            return make_response({"message": "Successfully responded to ticket"})
    else:
        email_response = send_email(
            ticket["email"],
            f"[pay2live] Support Ticket (ID: {str(ticket["_id"])})",
            f"A new response has been received.\n\nResponse:\n{response}",
        )
        if email_response["error"] is False:
            return make_response({"message": "Successfully responded to ticket"})
        else:
            return make_response(
                {
                    "message": f"Failed to respond to ticket as there was an error sending an email.",
                    "error": email_response["message"],
                },
                500,
            )
