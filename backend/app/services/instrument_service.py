from __future__ import annotations

from sqlmodel import Session

from app.models.instrument import Instrument
from app.repositories.instrument_repository import InstrumentRepository


class InstrumentService:
    def __init__(self, session: Session) -> None:
        self._repo = InstrumentRepository(session)

    def list_all(self) -> list[Instrument]:
        return self._repo.list_all()
