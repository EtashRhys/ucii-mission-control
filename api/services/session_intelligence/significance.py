def determine_session_significance(
    activity_level: str,
    session_pattern: str
):

    if (
        activity_level == "high"
        and session_pattern == "heartbeat_active"
    ):
        return "important"

    if (
        activity_level == "medium"
        or session_pattern == "browsing"
    ):
        return "relevant"

    return "routine"


def determine_significance_reason(
    session_significance: str,
    session_pattern: str
):

    if (
        session_significance == "important"
        and session_pattern == "heartbeat_active"
    ):
        return "active_engagement"

    if session_pattern == "browsing":
        return "multi_page_browsing"

    return "minimal_activity"


def determine_session_summary(
    significance_reason: str
):

    if significance_reason == "active_engagement":
        return "active_visitor_engagement"

    if significance_reason == "multi_page_browsing":
        return "visitor_browsing_activity"

    return "limited_interaction"
