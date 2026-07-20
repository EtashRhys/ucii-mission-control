from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.models import Event
from storage.database import get_database


router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)


@router.get("")
def query_sessions(
    limit: int = 50,
    visitor_id: str | None = None,
    database: Session = Depends(get_database)
):

    if limit > 100:
        limit = 100

    query = database.query(Event)

    if visitor_id:
        query = query.filter(
            Event.visitor_id == visitor_id
        )

    sessions = (
        query.with_entities(
            Event.session_id,
            Event.visitor_id,
            func.min(Event.created_at).label("first_seen"),
            func.max(Event.created_at).label("last_seen"),
            func.count(Event.id).label("event_count")
        )
        .group_by(
            Event.session_id,
            Event.visitor_id
        )
        .order_by(
            func.max(Event.created_at).desc()
        )
        .limit(limit)
        .all()
    )

    results = []

    for session in sessions:

        latest_event = (
            database.query(Event)
            .filter(
                Event.session_id == session.session_id,
                Event.visitor_id == session.visitor_id
            )
            .order_by(
                Event.created_at.desc()
            )
            .first()
        )

        results.append(
            {
                "session_id": session.session_id,
                "visitor_id": session.visitor_id,
                "first_seen": session.first_seen,
                "last_seen": session.last_seen,
                "event_count": session.event_count,
                "current_url": (
                    latest_event.url
                    if latest_event
                    else None
                ),
            }
        )

    return {
        "sessions": results
    }
