from email.message import EmailMessage
from typing import Any
import re
import smtplib
from app import smtp_host, smtp_password, smtp_port, smtp_sender, smtp_username


def send_email(
    recipient: str,
    subject: str,
    body: str,
    smtp_host: str = smtp_host,
    smtp_port: int = smtp_port,
    smtp_username: str = smtp_username,
    smtp_password: str = smtp_password,
    sender: str = smtp_sender,
) -> dict[str, Any]:
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            message = EmailMessage()
            message.set_content(body)
            message["Subject"] = subject
            message["From"] = sender
            message["To"] = recipient
            server.send_message(message)
        return {"error": False, "message": "Email sent successfully"}
    except Exception as e:
        return {"error": True, "message": str(e)}


# Use Luhn's algorithm to validate credit/debit card number
def luhn_check(card_number: str):
    card_number = str(card_number).replace(" ", "").replace("-", "")

    if not card_number.isdigit():
        return False

    total = 0
    reverse_digits = card_number[::-1]

    for i, digit in enumerate(reverse_digits):
        num = int(digit)

        if i % 2 == 1:
            num *= 2
            if num > 9:
                num -= 9

        total += num

    return total % 10 == 0


# Check credit/debit card types based on starting digits/lengths, using RegEx patterns
def get_card_type(card_number: str):
    card_number = str(card_number).replace(" ", "").replace("-", "")

    card_types = {
        "Visa": r"^4[0-9]{12}(?:[0-9]{3})?$",
        "MasterCard": r"^5[1-5][0-9]{14}$",
        "American Express": r"^3[47][0-9]{13}$",
        "Discover": r"^6(?:011|5[0-9]{2})[0-9]{12}$",
        "Diners Club": r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
        "JCB": r"^(?:2131|1800|35\d{3})\d{11}$",
        "Maestro": r"^(5[06789]|6[0-9])[0-9]{10,17}$",
        "UnionPay": r"^62[0-9]{14,17}$",
    }

    for card_type, pattern in card_types.items():
        if re.match(pattern, card_number):
            return card_type

    return "Unknown Card Type"


# Validate NRIC in Singapore based on its checksum
def validate_nric(input_str: Any) -> bool:
    try:
        if not isinstance(input_str, str) or len(input_str) != 9:
            return False

        nric = input_str.upper()
        pre = nric[0]
        digits = [int(num) for num in nric[1:8]]

        checkdigit = nric[8].upper()
        return checkdigit == get_check_digit(pre, digits)
    except Exception:
        return False


# Calculate the checksum for an NRIC in Singapore
def get_check_digit(pre: str, digits: list[int]) -> str | bool:
    weights = [2, 7, 6, 5, 4, 3, 2]
    check_ST = ["J", "Z", "I", "H", "G", "F", "E", "D", "C", "B", "A"]
    check_FG = ["X", "W", "U", "T", "R", "Q", "P", "N", "M", "L", "K"]
    check_M = ["X", "W", "U", "T", "R", "Q", "P", "N", "J", "L", "K"]

    total = sum(d * w for d, w in zip(digits, weights))

    offset = 0
    if pre in ["T", "G"]:
        offset = 4
    elif pre == "M":
        offset = 3

    d_value = (total + offset) % 11

    if pre in ["S", "T"]:
        return check_ST[d_value]
    elif pre in ["F", "G"]:
        return check_FG[d_value]
    elif pre == "M":
        return check_M[d_value]
    else:
        return False
