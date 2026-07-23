import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from api.models import Event
from api.models import Visitor
from api.schemas import EventCreate
from storage.database import get_database


router = APIRouter(
    prefix="/collect",
    tags=["events"]
)


def update_visitor(
    database: Session,
    event_data: EventCreate,
):

    metadata = event_data.metadata or {}

    visitor = (
        database.query(Visitor)
        .filter(
            Visitor.visitor_id == event_data.visitor_id
        )
        .first()
    )


    if visitor:

        visitor.last_seen = datetime.now(
            timezone.utc
        )

        visitor.visit_count += 1

        return visitor



    visitor = Visitor(

        visitor_id =
            event_data.visitor_id,

        first_seen =
            datetime.now(timezone.utc),

        last_seen =
            datetime.now(timezone.utc),

        visit_count =
            1,

        user_agent =
            metadata.get(
                "user_agent"
            ),

        platform =
            metadata.get(
                "platform"
            ),

        language =
            metadata.get(
                "language"
            ),

        timezone =
            metadata.get(
                "timezone"
            ),

        screen_width =
            metadata.get(
                "screen",
                {}
            ).get(
                "width"
            ),

        screen_height =
            metadata.get(
                "screen",
                {}
            ).get(
                "height"
            ),

        viewport_width =
            metadata.get(
                "viewport",
                {}
            ).get(
                "width"
            ),

        viewport_height =
            metadata.get(
                "viewport",
                {}
            ).get(
                "height"
            ),

        referrer =
            event_data.referrer

    )


    database.add(visitor)

    return visitor



@router.post("/event")
def collect_event(
    event_data: EventCreate,
    database: Session = Depends(get_database)
):

    event_id = str(uuid.uuid4())


    event = Event(

        event_id =
            event_id,

        event_type =
            event_data.event_type,

        visitor_id =
            event_data.visitor_id,

        session_id =
            event_data.session_id,

        url =
            event_data.url,

        referrer =
            event_data.referrer,

        metadata_json =
            json.dumps(
                event_data.metadata
            ),

        created_at =
            datetime.now(timezone.utc)

    )


    database.add(event)


    update_visitor(
        database,
        event_data
    )


    database.commit()


    database.refresh(event)


    return {

        "status":
            "accepted",

        "event_id":
            event.event_id

    }
