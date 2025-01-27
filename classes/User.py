from typing import Any


class User:
    def __init__(
        self,
        phone: str | None,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        gender: str | None = None,
        nric: str | None = None,
        role: str | None = "patient",
        address: str | None = None,
        session_token: str | None = None,
        otp: str | None = None,
        admin: bool = False,
        registered: bool = False,
        active: bool = True,
    ) -> None:
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.gender = gender
        self.nric = nric
        self.role = role
        self.address = address
        self.session_token = session_token
        self.otp = otp
        self.admin = admin
        self.registered = registered
        self.active = active

    def to_dict(self) -> dict[str, Any]:
        return {
            "phone": self.phone,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "gender": self.gender,
            "nric": self.nric,
            "role": self.role,
            "address": self.address,
            "session_token": self.session_token,
            "otp": self.otp,
            "admin": self.admin,
            "registered": self.registered,
            "active": self.active,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        return cls(
            phone=data.get("phone"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            email=data.get("email"),
            gender=data.get("gender"),
            nric=data.get("nric"),
            role=data.get("role"),
            address=data.get("address"),
            session_token=data.get("session_token"),
            otp=data.get("otp"),
            admin=data.get("admin") == "True",
            registered=data.get("registered") == "True",
            active=data.get("active") == "True",
        )
