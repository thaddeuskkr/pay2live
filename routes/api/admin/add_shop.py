from flask import request, make_response
from app import app, users, shop


@app.route("/api/admin/shop/add", methods=["POST"])
def a_add_shop():
    session_token = request.cookies.get("session_token")
    user = users.find_one({"session_token": session_token}) if session_token else None
    if not user:
        return make_response({"message": "Invalid session token"}, 401)
    if not user["admin"]:
        return make_response({"message": "Unauthorized"})
    data = request.get_json()
    required_fields = [
        "name",
        "price",
        "visible",
        "image",
    ]
    missing_keys = set(required_fields - data.keys())
    if missing_keys:
        return make_response(
            {"message": f"Missing required fields: {missing_keys}"}, 400
        )
    name: str = data.get("name")
    price: str | float = data.get("price")
    visible: str = data.get("visible")
    image: str = data.get("image")

    if visible not in ["true", "false"]:
        return make_response({"message": "Invalid visibility"}, 400)

    if image and not image.startswith("https://"):
        return make_response({"message": "Invalid image URL"}, 400)

    try:
        price = float(price)
    except ValueError:
        return make_response({"message": "Invalid price"}, 400)

    shop.insert_one(
        {
            "name": name,
            "price": price,
            "visible": visible == "true",
            "image": image,
        },
    )

    return make_response({"message": "Item added successfully"}, 200)
