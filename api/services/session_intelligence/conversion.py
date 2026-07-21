from typing import Dict, Any, List


def analyze_conversion_signal(
    journey: Dict[str, Any],
    outcome: Dict[str, Any],
    activity: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Derive visitor conversion intent from existing intelligence layers.

    This is intentionally rule-based in Phase 5.0.10.
    The goal is creating the primitive representation,
    not building predictive analytics.
    """

    signals: List[str] = []

    confidence_score = 0

    journey_stage = (
        journey.get("journey_stage")
        or journey.get("stage")
        or ""
    ).lower()

    outcome_type = (
        outcome.get("outcome")
        or outcome.get("outcome_type")
        or ""
    ).lower()

    activity = activity or {}

    pages = activity.get("pages", [])
    if not isinstance(pages, list):
        pages = []

    page_text = " ".join(str(page).lower() for page in pages)

    if any(
        keyword in page_text
        for keyword in [
            "docs",
            "documentation",
            "api",
            "developer",
            "reference",
        ]
    ):
        signals.append("documentation_access")
        confidence_score += 2

    if (
        "return" in journey_stage
        or journey.get("returning") is True
    ):
        signals.append("return_visit")
        confidence_score += 1

    if (
        "deep" in outcome_type
        or "exploration" in outcome_type
        or "research" in journey_stage
    ):
        signals.append("deep_navigation")
        confidence_score += 1

    if confidence_score >= 4:
        state = "technical_validation"
        confidence = "high"

    elif confidence_score >= 2:
        state = "evaluation"
        confidence = "medium"

    elif confidence_score == 1:
        state = "interest"
        confidence = "low"

    else:
        state = "awareness"
        confidence = "low"

    return {
        "state": state,
        "confidence": confidence,
        "signals": signals,
    }
