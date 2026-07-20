# UCII Mission Control Architecture

## Purpose

UCII Mission Control is the operational observability layer for UCII.

UCII provides identity primitives.

Mission Control provides operational visibility primitives.


## Core Principle

Events are the foundation.

Dashboards, analytics, and insights are derived from event data.


## Architecture

Browser

↓

Tracker SDK

↓

Event Collection API

↓

Storage Layer

↓

Mission Control API

↓

Dashboard


## Design Principles

- Event-first architecture
- Self-hosted infrastructure
- Minimal dependencies
- Privacy-respecting collection
- Expandable event schema


## Version 1 Scope

Included:

- Event ingestion
- Event storage
- Session reconstruction
- Campaign attribution
- Operational dashboard


Excluded:

- AI summaries
- Alerts
- Reports
- User accounts
- Billing
