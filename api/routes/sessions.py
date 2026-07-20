import json
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
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

    now = datetime.now(timezone.utc)

    ACTIVE_THRESHOLD_SECONDS = 300

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

        duration_seconds = int(
            (
                session.last_seen - session.first_seen
            ).total_seconds()
        )

        last_seen = session.last_seen

        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(
                tzinfo=timezone.utc
            )

        last_activity_seconds_ago = int(
            (
                now - last_seen
            ).total_seconds()
        )

        status = (
            "active"
            if last_activity_seconds_ago <= ACTIVE_THRESHOLD_SECONDS
            else "inactive"
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
                "duration_seconds": duration_seconds,
                "last_activity_seconds_ago": last_activity_seconds_ago,
                "status": status,
            }
        )

    return {
        "sessions": results
    }


@router.get("/{session_id}")
def get_session(
    session_id: str,
    database: Session = Depends(get_database)
):

    events = (
        database.query(Event)
        .filter(
            Event.session_id == session_id
        )
        .order_by(
            Event.created_at.asc()
        )
        .all()
    )

    if not events:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    event_results = []

    for event in events:

        metadata = {}

        if event.metadata_json:
            try:
                metadata = json.loads(event.metadata_json)
            except json.JSONDecodeError:
                metadata = {}

        event_results.append(
            {
                "event_type": event.event_type,
                "url": event.url,
                "referrer": event.referrer,
                "metadata": metadata,
                "created_at": event.created_at,
            }
        )

    return {
        "session_id": session_id,
        "visitor_id": events[0].visitor_id,
        "first_seen": events[0].created_at,
        "last_seen": events[-1].created_at,
        "event_count": len(events),
        "events": event_results
    }
