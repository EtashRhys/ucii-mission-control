def determine_outcome_signal(
    pages_viewed,
    unique_paths,
    intent_signal,
    journey_pattern,
    session_pattern
):
    if intent_signal in [
        "documentation_exploration",
        "active_testing",
    ]:
        return "documentation_access"

    if journey_pattern == "heartbeat_session":
        return "high_intent"

    if pages_viewed > 1:
        return "exploration"

    return "no_outcome"


def determine_outcome_depth(
    pages_viewed,
    event_count,
    journey_depth
):
    if journey_depth == "deep" and event_count > 20:
        return "deep"

    if pages_viewed > 1 or event_count > 5:
        return "moderate"

    if event_count > 0:
        return "shallow"

    return "none"


def determine_outcome_reason(
    outcome_signal
):
    reasons = {
        "documentation_access":
            "visitor accessed informational resources",

        "high_intent":
            "visitor demonstrated sustained engagement",

        "exploration":
            "visitor explored multiple areas",

        "no_outcome":
            "visitor did not complete a meaningful action",
    }

    return reasons.get(
        outcome_signal,
        "unknown"
    )
