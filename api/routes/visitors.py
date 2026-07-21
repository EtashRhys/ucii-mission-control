from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.models import Event
from storage.database import get_database

from api.services.visitor_intelligence.profile import (
    build_visitor_profile,
)

from api.services.visitor_intelligence.segmentation import (
    determine_visitor_segment,
)

from api.services.session_intelligence.journey import (
    determine_journey_depth,
    determine_return_behavior,
)

from api.services.session_intelligence.conversion import (
    analyze_conversion_signal,
)


router = APIRouter(
    prefix="/visitors",
    tags=["visitors"]
)


@router.get("/{visitor_id}/profile")
def get_visitor_profile(
    visitor_id: str,
    database: Session = Depends(get_database)
):

    sessions = (
        database.query(Event.session_id)
        .filter(
            Event.visitor_id == visitor_id
        )
        .distinct()
        .all()
    )

    if not sessions:
        return {
            "visitor_id": visitor_id,
            "visitor_profile": {
                "visitor_type": "unknown",
                "engagement_pattern": "unknown",
                "conversion_readiness": "unknown",
                "confidence": "low",
            }
        }


    session_profiles = []


    for session in sessions:

        events = (
            database.query(Event)
            .filter(
                Event.session_id == session.session_id,
                Event.visitor_id == visitor_id
            )
            .order_by(
                Event.created_at.asc()
            )
            .all()
        )

        event_count = len(events)

        pages = [
            event.url
            for event in events
            if event.url
        ]


        first_seen = events[0].created_at
        last_seen = events[-1].created_at


        duration_seconds = int(
            (
                last_seen - first_seen
            ).total_seconds()
        )


        journey_depth = determine_journey_depth(
            event_count,
            len(pages),
            duration_seconds
        )


        return_behavior = determine_return_behavior(
            event_count,
            first_seen,
            last_seen
        )


        conversion_signal = analyze_conversion_signal(
            {
                "journey_depth": journey_depth,
                "return_behavior": return_behavior,
            },
            {},
            {
                "pages": pages
            }
        )


        session_profiles.append(
            {
                "journey_depth": journey_depth,
                "return_behavior": return_behavior,
                "conversion_signal": conversion_signal.get(
                    "conversion_signal",
                    {}
                ),
            }
        )


    profile = build_visitor_profile(
        session_profiles
    )

    visitor_segment = determine_visitor_segment(
        profile
    )

    profile["segment"] = visitor_segment


    return {
        "visitor_id": visitor_id,
        "visitor_profile": profile,
    }
