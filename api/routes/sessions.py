import json
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.models import Event
from storage.database import get_database

from api.services.session_intelligence.activity import determine_activity_level
from api.services.session_intelligence.classification import determine_session_pattern
from api.services.session_intelligence.significance import (
    determine_session_significance,
    determine_significance_reason,
    determine_session_summary,
)
from api.services.session_intelligence.intent import determine_intent_signal
from api.services.session_intelligence.health import determine_session_health
from api.services.session_intelligence.reliability import determine_reliability_signal
from api.services.session_intelligence.timeline import build_session_timeline
from api.services.session_intelligence.journey import (
    determine_journey_pattern,
    determine_journey_depth,
    determine_navigation_style,
    determine_return_behavior,
)
from api.services.session_intelligence.outcome import (
    determine_outcome_signal,
    determine_outcome_depth,
    determine_outcome_reason,
)
from api.services.session_intelligence.conversion import (
    analyze_conversion_signal,
)


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

        session_events = (
            database.query(Event)
            .filter(
                Event.session_id == session.session_id,
                Event.visitor_id == session.visitor_id
            )
            .order_by(
                Event.created_at.asc()
            )
            .all()
        )

        latest_event = (
            session_events[-1]
            if session_events
            else None
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

        pages_viewed = (
            database.query(func.count(Event.id))
            .filter(
                Event.session_id == session.session_id,
                Event.event_type == "page_view"
            )
            .scalar()
        )

        unique_paths = (
            database.query(func.count(func.distinct(Event.url)))
            .filter(
                Event.session_id == session.session_id
            )
            .scalar()
        )

        last_event_type = (
            latest_event.event_type
            if latest_event
            else None
        )

        activity_level = determine_activity_level(
            session.event_count
        )

        session_pattern = determine_session_pattern(
            last_event_type,
            pages_viewed,
            session.event_count
        )

        session_significance = determine_session_significance(
            activity_level,
            session_pattern
        )

        significance_reason = determine_significance_reason(
            session_significance,
            session_pattern
        )

        session_summary = determine_session_summary(
            significance_reason
        )

        intent_signal = determine_intent_signal(
            session.event_count,
            latest_event.url if latest_event else None,
            pages_viewed,
            last_event_type,
            activity_level,
            session_pattern
        )

        session_health = determine_session_health(
            session.event_count,
            activity_level,
            status,
            1 if status == "active" else 0
        )

        reliability_signal = determine_reliability_signal(
            session_health,
            session_pattern,
            activity_level,
            status
        )

        journey_pattern = determine_journey_pattern(
            session_events,
            pages_viewed,
            activity_level
        )

        journey_depth = determine_journey_depth(
            session.event_count,
            pages_viewed,
            duration_seconds
        )

        navigation_style = determine_navigation_style(
            journey_pattern,
            pages_viewed,
            activity_level
        )

        return_behavior = determine_return_behavior(
            session.event_count,
            session.first_seen,
            session.last_seen
        )

        outcome_signal = determine_outcome_signal(
            pages_viewed,
            unique_paths,
            intent_signal,
            journey_pattern,
            session_pattern
        )

        outcome_depth = determine_outcome_depth(
            pages_viewed,
            session.event_count,
            journey_depth
        )

        outcome_reason = determine_outcome_reason(
            outcome_signal
        )

        conversion_signal = analyze_conversion_signal(
            {
                "journey_pattern": journey_pattern,
                "journey_depth": journey_depth,
                "navigation_style": navigation_style,
                "return_behavior": return_behavior,
            },
            {
                "outcome_signal": outcome_signal,
                "outcome_depth": outcome_depth,
                "outcome_reason": outcome_reason,
            },
            {
                "pages": [
                    event.url
                    for event in session_events
                    if event.url
                ]
            }
        )

        timeline = build_session_timeline(
            session_events
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
                "pages_viewed": pages_viewed,
                "unique_paths": unique_paths,
                "last_event_type": last_event_type,
                "activity_level": activity_level,
                "session_pattern": session_pattern,
                "session_significance": session_significance,
                "significance_reason": significance_reason,
                "session_summary": session_summary,
                "intent_signal": intent_signal,
                "session_health": session_health,
                "reliability_signal": reliability_signal,
                "journey_pattern": journey_pattern,
                "journey_depth": journey_depth,
                "navigation_style": navigation_style,
                "return_behavior": return_behavior,
                "outcome_signal": outcome_signal,
                "outcome_depth": outcome_depth,
                "outcome_reason": outcome_reason,
                "conversion_signal": conversion_signal,
                "timeline": timeline,
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

    timeline = build_session_timeline(events)

    return {
        "session_id": session_id,
        "visitor_id": events[0].visitor_id,
        "first_seen": events[0].created_at,
        "last_seen": events[-1].created_at,
        "event_count": len(events),
        "events": event_results,
        "timeline": timeline
    }
