from typing import Dict, Any, List


def determine_visitor_segment(
    profile: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Classify a visitor into an operational segment.

    Phase 5.0.12:
    deterministic rule-based visitor segmentation.

    This layer groups existing visitor profiles
    into actionable operational categories.
    """

    signals: List[str] = []

    visitor_type = (
        profile.get("visitor_type")
        or ""
    )

    engagement_pattern = (
        profile.get("engagement_pattern")
        or ""
    )

    conversion_readiness = (
        profile.get("conversion_readiness")
        or ""
    )

    profile_signals = (
        profile.get("signals")
        or []
    )

    if not isinstance(profile_signals, list):
        profile_signals = []


    if (
        visitor_type == "technical_evaluator"
        or conversion_readiness == "high"
        or "technical_research_behavior" in profile_signals
    ):
        signals.append(
            "technical_evaluation"
        )

        return {
            "segment": "technical_evaluator",
            "confidence": "high",
            "signals": signals,
        }


    if (
        engagement_pattern == "returning_researcher"
        or "repeat_engagement" in profile_signals
    ):
        signals.append(
            "repeat_engagement"
        )

        return {
            "segment": "returning_researcher",
            "confidence": "medium",
            "signals": signals,
        }


    if (
        engagement_pattern == "deep_exploration"
        or visitor_type == "explorer"
    ):
        signals.append(
            "deep_exploration"
        )

        return {
            "segment": "engaged_explorer",
            "confidence": "medium",
            "signals": signals,
        }


    signals.append(
        "limited_engagement"
    )

    return {
        "segment": "casual_observer",
        "confidence": "low",
        "signals": signals,
    }
