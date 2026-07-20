def determine_reliability_signal(
    session_health,
    session_pattern,
    activity_level,
    status,
):
    """
    Determine session reliability.

    Deterministic interpretation layer.

    Evaluates existing session intelligence primitives only.

    Returns:

    stable:
        Session behavior appears consistent.

    unstable:
        Session behavior exists but appears inconsistent.

    interrupted:
        Session activity appears to have stopped.

    unknown:
        Insufficient signal.
    """

    if (
        session_health == "healthy"
        and session_pattern == "heartbeat_active"
        and status == "active"
    ):
        return "stable"

    if (
        session_health in ("stale", "degraded")
        and status == "inactive"
    ):
        return "interrupted"

    if (
        activity_level in ("high", "medium")
        and session_health == "degraded"
    ):
        return "unstable"

    return "unknown"
