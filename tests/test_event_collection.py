import pytest

from httpx import ASGITransport
from httpx import AsyncClient

from api.main import app


@pytest.mark.anyio
async def test_event_collection():

    transport = ASGITransport(
        app=app
    )

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:

        response = await client.post(
            "/collect/event",
            json={
                "event_type": "page_view",
                "visitor_id": "visitor_123",
                "session_id": "session_456",
                "url": "/docs",
                "referrer": "github",
                "metadata": {
                    "campaign": "launch"
                }
            }
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "accepted"
    assert "event_id" in body
