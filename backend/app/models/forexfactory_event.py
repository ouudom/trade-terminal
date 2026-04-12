from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel
from sqlalchemy import UniqueConstraint


class ForexFactoryEvent(SQLModel, table=True):
    __tablename__ = "forexfactory_events"
    __table_args__ = (
        UniqueConstraint("currency", "event_name", "date", name="uq_ff_event"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    currency: str = Field(max_length=10)
    event_name: str = Field(max_length=200)
    date: Optional[str] = Field(default=None, max_length=50)
    time: Optional[str] = Field(default=None, max_length=20)
    impact: str = Field(max_length=20)
    actual: Optional[str] = Field(default=None, max_length=50)
    forecast: Optional[str] = Field(default=None, max_length=50)
    previous: Optional[str] = Field(default=None, max_length=50)
    fetched_at: datetime = Field(default_factory=datetime.utcnow)
