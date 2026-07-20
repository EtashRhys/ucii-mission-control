from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from storage.database import Base


class Event(Base):

    __tablename__ = "events"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    event_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )


    event_type = Column(
        String,
        index=True,
        nullable=False
    )


    visitor_id = Column(
        String,
        index=True,
        nullable=False
    )


    session_id = Column(
        String,
        index=True,
        nullable=False
    )


    url = Column(
        String,
        nullable=True
    )


    referrer = Column(
        String,
        nullable=True
    )


    metadata_json = Column(
        Text,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
