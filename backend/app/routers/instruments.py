from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.core.database import get_session
from app.models.instrument import Instrument

router = APIRouter(prefix="/instruments", tags=["instruments"])


@router.get("", response_model=list[Instrument])
def list_instruments(session: Session = Depends(get_session)):
    return session.exec(select(Instrument)).all()
