def determine_intent_signal(
    event_count: int,
    current_url: str | None,
    pages_viewed: int,
    last_event_type: str | None,
    activity_level: str,
    session_pattern: str
):

    if (
        event_count > 50
        and last_event_type == "heartbeat"
        and activity_level == "high"
    ):
        return "active_testing"

    if (
        current_url
        and "/docs" in current_url
        and pages_viewed > 1
    ):
        return "documentation_exploration"

    if (
        session_pattern == "heartbeat_active"
        and event_count > 10
    ):
        return "feature_usage"

    if (
        activity_level == "low"
        and pages_viewed <= 2
    ):
        return "idle_browsing"

    return "unknown"
