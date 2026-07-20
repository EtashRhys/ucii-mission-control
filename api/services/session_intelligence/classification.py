def determine_session_pattern(
    last_event_type: str | None,
    pages_viewed: int,
    event_count: int
):

    if (
        last_event_type == "heartbeat"
        and pages_viewed < event_count
    ):
        return "heartbeat_active"

    if pages_viewed > 1:
        return "browsing"

    return "single_page"
