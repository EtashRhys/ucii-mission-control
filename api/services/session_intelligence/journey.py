def determine_journey_pattern(
    events,
    pages_viewed,
    activity_level
):
    """
    Determine high-level visitor journey pattern.
    """

    event_types = [
        event.event_type
        for event in events
    ]

    if pages_viewed <= 1:
        if "heartbeat" in event_types:
            return "heartbeat_session"

        return "single_page_visit"

    if pages_viewed > 1:
        return "multi_page_navigation"

    return "unknown"


def determine_journey_depth(
    event_count,
    pages_viewed,
    duration_seconds
):
    """
    Determine journey depth.
    """

    if (
        event_count >= 20
        or pages_viewed >= 5
        or duration_seconds >= 900
    ):
        return "deep"

    if (
        event_count >= 5
        or pages_viewed >= 2
        or duration_seconds >= 120
    ):
        return "moderate"

    return "shallow"


def determine_navigation_style(
    journey_pattern,
    pages_viewed,
    activity_level
):
    """
    Determine navigation behavior style.
    """

    if journey_pattern == "multi_page_navigation":
        return "exploratory"

    if activity_level == "high":
        return "focused"

    return "passive"


def determine_return_behavior(
    event_count,
    first_seen,
    last_seen
):
    """
    Initial placeholder for return detection.

    Future versions will use visitor history.
    """

    if event_count > 1:
        return "returning_session"

    return "first_visit"
