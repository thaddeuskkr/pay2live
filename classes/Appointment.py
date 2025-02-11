from typing import Any, Optional
from bson import ObjectId

class Appointment:
    def __init__(
        self,
        user_id: ObjectId,
        service: str,
        timestamp: int,
        doctor_id: Optional[ObjectId] = None,
    ) -> None:
        self.user_id = user_id
        self.service = service
        self.timestamp = timestamp
        self.doctor_id = doctor_id

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "service": self.service,
            "timestamp": self.timestamp,
            "doctor_id": self.doctor_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Appointment":
        return cls(
            user_id=ObjectId(data.get("user_id")),
            service=data.get("service"),
            timestamp=int(data.get("timestamp")),
            doctor_id=ObjectId(data.get("doctor_id")) if data.get("doctor_id") else None,
        )