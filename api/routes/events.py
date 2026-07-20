import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.models import Event
from api.schemas import EventCreate
from storage.database import get_database


router = APIRouter(
    prefix="/collect",
    tags=["events"]
)


@router.post("/event")
def collect_event(
    event_data: EventCreate,
    database: Session = Depends(get_database)
):

    event_id = str(uuid.uuid4())

    event = Event(
        event_id=event_id,
        event_type=event_data.event_type,
        visitor_id=event_data.visitor_id,
        session_id=event_data.session_id,
        url=event_data.url,
        referrer=event_data.referrer,
        metadata_json=json.dumps(
            event_data.metadata
        ),
        created_at=datetime.now(timezone.utc)
    )

    database.add(event)

    database.commit()

    database.refresh(event)

    return {
        "status": "accepted",
        "event_id": event.event_id
    }
