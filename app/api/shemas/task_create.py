from typing import Any, Dict

from pydantic import BaseModel, Field, field_validator

MAX_PAYLOAD_SIZE = 10


class TaskCreate(BaseModel):
    payload: Dict[str, Any]

    class Config:
        from_attributes = True

    @field_validator("payload")
    def validate_payload(cls, value):
        if not value:
            raise ValueError("payload не может быть пустым")
        if len(value) > MAX_PAYLOAD_SIZE:
            raise ValueError(f"Payload too large: max {MAX_PAYLOAD_SIZE} keys")
        return value
