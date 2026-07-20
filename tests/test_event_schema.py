import pytest

from pydantic import ValidationError

from api.schemas import EventCreate


def test_valid_event_schema():

    event = EventCreate(
        event_type="page_view",
        visitor_id="visitor_123",
        session_id="session_456",
        url="/docs",
        metadata={
            "campaign": "launch"
        }
    )

    assert event.event_type == "page_view"
    assert event.metadata["campaign"] == "launch"


def test_invalid_event_missing_required_fields():

    with pytest.raises(ValidationError):

        EventCreate(
            event_type="page_view"
        )
