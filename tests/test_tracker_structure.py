from pathlib import Path


def test_tracker_file_exists():
    tracker_file = Path("tracker/ucii-tracker.js")

    assert tracker_file.exists(), (
        "UCII tracker SDK file is missing"
    )


def test_tracker_exposes_global_object():
    tracker_file = Path("tracker/ucii-tracker.js")

    content = tracker_file.read_text()

    assert "window.UCIITracker" in content, (
        "UCIITracker global object missing"
    )


def test_tracker_initialization_exists():
    tracker_file = Path("tracker/ucii-tracker.js")

    content = tracker_file.read_text()

    assert "init(options)" in content, (
        "UCIITracker.init missing"
    )


def test_tracker_event_collection_exists():
    tracker_file = Path("tracker/ucii-tracker.js")

    content = tracker_file.read_text()

    assert "sendEvent" in content, (
        "Event sender missing"
    )

    assert "event_type" in content, (
        "Event schema missing"
    )


def test_tracker_v1_events_exist():
    tracker_file = Path("tracker/ucii-tracker.js")

    content = tracker_file.read_text()

    required_events = [
        "page_view",
        "heartbeat",
        "page_leave",
    ]

    for event in required_events:
        assert event in content, (
            f"Missing tracker event: {event}"
        )
