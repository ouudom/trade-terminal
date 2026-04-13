from __future__ import annotations

from sqlmodel import Session, select

from app.models.instrument import Instrument


class InstrumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_all(self) -> list[Instrument]:
        return self._session.exec(select(Instrument)).all()

    def get_by_id(self, id: int) -> Instrument | None:
        return self._session.get(Instrument, id)

    def get_by_symbol(self, symbol: str) -> Instrument | None:
        return self._session.exec(
            select(Instrument).where(Instrument.symbol == symbol)
        ).first()
