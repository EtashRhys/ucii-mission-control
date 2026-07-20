def determine_session_health(
    event_count,
    activity_level,
    session_status,
    heartbeat_count,
):
    """
    Determine the operational health of a session.

    Deterministic interpretation layer.

    Evaluates existing session primitives only.

    Returns:

    healthy:
        Session appears active and behaving normally.

    degraded:
        Session has activity but shows weaker continuity.

    stale:
        Session appears inactive or abandoned.
    """

    if (
        session_status == "inactive"
        and heartbeat_count == 0
        and event_count == 0
    ):
        return "stale"

    if (
        activity_level == "high"
        and heartbeat_count > 0
        and event_count > 0
    ):
        return "healthy"

    if (
        activity_level == "medium"
        and heartbeat_count > 0
    ):
        return "healthy"

    if (
        event_count > 0
        or heartbeat_count > 0
    ):
        return "degraded"

    return "stale"
