from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.models import Event
from storage.database import get_database


router = APIRouter(
    prefix="/events",
    tags=["query"]
)


@router.get("")
def query_events(
    limit: int = 50,
    database: Session = Depends(get_database)
):

    if limit > 100:
        limit = 100

    events = (
        database.query(Event)
        .order_by(
            Event.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "events": [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "visitor_id": event.visitor_id,
                "session_id": event.session_id,
                "url": event.url,
                "referrer": event.referrer,
                "created_at": event.created_at,
            }
            for event in events
        ]
    }
