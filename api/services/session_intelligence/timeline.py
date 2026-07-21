from datetime import datetime


def build_session_timeline(events):
    """
    Convert raw session events into an ordered timeline.
    """

    timeline = []

    for event in sorted(events, key=lambda x: x.created_at):
        timeline.append(
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "url": event.url,
                "created_at": (
                    event.created_at.isoformat()
                    if isinstance(event.created_at, datetime)
                    else event.created_at
                ),
            }
        )

    return timeline
