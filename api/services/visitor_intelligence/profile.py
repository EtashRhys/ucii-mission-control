from typing import Dict, Any, List


def build_visitor_profile(
    sessions: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Build a visitor intelligence profile
    from accumulated session intelligence.

    Phase 5.0.11:
    deterministic rule-based classification.
    """

    signals = []

    if not sessions:
        return {
            "visitor_type": "unknown",
            "engagement_pattern": "unknown",
            "conversion_readiness": "unknown",
            "confidence": "low",
        }

    technical_sessions = 0
    returning_sessions = 0
    deep_sessions = 0

    for session in sessions:

        conversion = session.get(
            "conversion_signal",
            {}
        )

        journey_depth = session.get(
            "journey_depth"
        )

        return_behavior = session.get(
            "return_behavior"
        )

        if (
            conversion.get("state")
            in [
                "evaluation",
                "technical_validation",
            ]
        ):
            technical_sessions += 1

        if return_behavior == "returning_session":
            returning_sessions += 1

        if journey_depth == "deep":
            deep_sessions += 1


    if technical_sessions >= 1 and deep_sessions >= 1:
        visitor_type = "technical_evaluator"
        signals.append(
            "technical_research_behavior"
        )

    elif returning_sessions >= 1:
        visitor_type = "returning_visitor"
        signals.append(
            "repeat_engagement"
        )

    else:
        visitor_type = "explorer"


    if returning_sessions >= 2:
        engagement_pattern = (
            "returning_researcher"
        )

    elif deep_sessions >= 1:
        engagement_pattern = (
            "deep_exploration"
        )

    else:
        engagement_pattern = (
            "initial_exploration"
        )


    if technical_sessions >= 2:
        conversion_readiness = "high"

    elif technical_sessions == 1:
        conversion_readiness = "medium"

    else:
        conversion_readiness = "low"


    confidence = (
        "high"
        if len(sessions) >= 3
        else "medium"
        if len(sessions) >= 1
        else "low"
    )


    return {
        "visitor_type": visitor_type,
        "engagement_pattern": engagement_pattern,
        "conversion_readiness": conversion_readiness,
        "confidence": confidence,
        "signals": signals,
    }
