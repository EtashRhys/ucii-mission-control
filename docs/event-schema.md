# UCII Mission Control Event Schema

## Event Philosophy

Everything becomes an event.

The ingestion layer remains stable while event types expand.


## Initial Events

- page_view
- page_leave
- heartbeat
- scroll_depth


## Future Events

- identity_created
- credential_registered
- credential_verified
- verification_failed
- api_request
- health_check
- x402_payment
- email_verified


## Base Event Structure

```json
{
  "event_id": "uuid",
  "event_type": "page_view",
  "timestamp": "ISO-8601",

  "visitor_id": "anonymous-id",
  "session_id": "session-id",

  "url": "/docs",
  "referrer": "",

  "metadata": {}
}
