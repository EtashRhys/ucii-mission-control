from typing import Any

from pydantic import BaseModel
from pydantic import Field


class EventCreate(BaseModel):

    event_type: str = Field(
        ...,
        min_length=1
    )

    visitor_id: str = Field(
        ...,
        min_length=1
    )

    session_id: str = Field(
        ...,
        min_length=1
    )

    url: str | None = None

    referrer: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )
