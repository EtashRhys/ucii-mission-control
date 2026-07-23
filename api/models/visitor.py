from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from storage.database import Base


class Visitor(Base):

    __tablename__ = "visitors"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    visitor_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )


    first_seen = Column(
        DateTime,
        default=datetime.utcnow
    )


    last_seen = Column(
        DateTime,
        default=datetime.utcnow
    )


    visit_count = Column(
        Integer,
        default=1
    )


    user_agent = Column(
        String,
        nullable=True
    )


    platform = Column(
        String,
        nullable=True
    )


    language = Column(
        String,
        nullable=True
    )


    timezone = Column(
        String,
        nullable=True
    )


    screen_width = Column(
        Integer,
        nullable=True
    )


    screen_height = Column(
        Integer,
        nullable=True
    )


    viewport_width = Column(
        Integer,
        nullable=True
    )


    viewport_height = Column(
        Integer,
        nullable=True
    )


    referrer = Column(
        String,
        nullable=True
    )
