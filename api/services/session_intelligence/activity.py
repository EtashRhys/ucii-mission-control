def determine_activity_level(
    event_count: int
):

    if event_count >= 20:
        return "high"

    if event_count >= 5:
        return "medium"

    return "low"
