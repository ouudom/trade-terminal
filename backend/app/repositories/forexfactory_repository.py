from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, select

from app.models.forexfactory_event import ForexFactoryEvent


class ForexFactoryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def upsert_events(self, events: list[dict]) -> int:
        """
        Upsert Medium/High impact events.
        Unique key: (currency, event_name, date).
        On conflict: update actual, forecast, previous, time, fetched_at.
        Returns count of rows upserted.
        """
        STORED_IMPACTS = {"High", "Medium"}
        to_store = [e for e in events if e.get("impact") in STORED_IMPACTS]
        if not to_store:
            return 0

        now = datetime.utcnow()

        # Deduplicate by unique constraint key
        seen: set[tuple] = set()
        rows = []
        for e in to_store:
            key = (e["currency"], e["event"], e["date"])
            if key not in seen:
                seen.add(key)
                rows.append({
                    "currency":   e["currency"],
                    "event_name": e["event"],
                    "date":       e["date"],
                    "time":       e["time"],
                    "impact":     e["impact"],
                    "actual":     e["actual"],
                    "forecast":   e["forecast"],
                    "previous":   e["previous"],
                    "fetched_at": now,
                })

        if not rows:
            return 0

        stmt = pg_insert(ForexFactoryEvent).values(rows)
        stmt = stmt.on_conflict_do_update(
            constraint="uq_ff_event",
            set_={
                "time":       stmt.excluded.time,
                "actual":     stmt.excluded.actual,
                "forecast":   stmt.excluded.forecast,
                "previous":   stmt.excluded.previous,
                "fetched_at": stmt.excluded.fetched_at,
            },
        )
        self._session.execute(stmt)
        self._session.commit()
        return len(rows)

    def get_events(
        self, currency: Optional[str] = None, impact: Optional[str] = None
    ) -> list[ForexFactoryEvent]:
        stmt = select(ForexFactoryEvent)
        if currency:
            stmt = stmt.where(ForexFactoryEvent.currency == currency.upper())
        if impact:
            stmt = stmt.where(ForexFactoryEvent.impact == impact.capitalize())
        return self._session.exec(stmt).all()
