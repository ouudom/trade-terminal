import re
from datetime import datetime, timedelta
from typing import List, Optional

import httpx
from bs4 import BeautifulSoup
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.forexfactory_event import ForexFactoryEvent

router = APIRouter(prefix="/forexfactory", tags=["ForexFactory"])

FF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.forexfactory.com/",
    "Accept": "text/html,application/xhtml+xml",
}

_IMPACT_CLASS_MAP = {
    "icon--ff-impact-red": "High",
    "icon--ff-impact-ora": "Medium",
    "icon--ff-impact-yel": "Low",
    "icon--ff-impact-gra": "Non-economic",
}

STORED_IMPACTS = {"High", "Medium"}


class ForexEvent(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    currency: Optional[str] = None
    impact: Optional[str] = None
    event: Optional[str] = None
    actual: Optional[str] = None
    forecast: Optional[str] = None
    previous: Optional[str] = None


def _text(el) -> Optional[str]:
    if el is None:
        return None
    t = el.get_text(strip=True)
    return t if t else None


def _ff_week_param(week: str) -> str:
    """
    FF HTML calendar expects a specific Sunday date, e.g. 'mar30.2025'.
    Convert 'this week' / 'last week' / 'next week' to that format.
    FF weeks start on Sunday (weekday index 6).
    """
    today = datetime.utcnow().date()
    # days since last Sunday: Mon=1, Tue=2, ..., Sun=0
    days_since_sunday = (today.weekday() + 1) % 7
    this_sunday = today - timedelta(days=days_since_sunday)

    if week == "last week":
        start = this_sunday - timedelta(weeks=1)
    elif week == "next week":
        start = this_sunday + timedelta(weeks=1)
    else:
        start = this_sunday

    # e.g. "mar30.2025"
    return start.strftime("%b%d.%Y").lower()


def _parse_date(raw: Optional[str]) -> Optional[str]:
    """Convert FF date strings like 'Mon Mar 31' or 'Apr 2' → 'YYYY-MM-DD'.
    Handles year rollover: if the parsed month is > 6 months from today, adjust year.
    """
    if not raw:
        return None
    m = re.search(r"([A-Za-z]{3})\s+(\d{1,2})", raw)
    if not m:
        return raw
    month_s, day_s = m.group(1), m.group(2)
    today = datetime.utcnow()
    for year_offset in (0, 1, -1):
        try:
            dt = datetime.strptime(f"{month_s} {day_s} {today.year + year_offset}", "%b %d %Y")
            # Pick the year that keeps the date within ~6 months of today
            if abs((dt.date() - today.date()).days) <= 200:
                return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return raw


def _impact(row) -> Optional[str]:
    span = row.select_one(".calendar__impact span")
    if span is None:
        return None
    for cls in span.get("class", []):
        if cls in _IMPACT_CLASS_MAP:
            return _IMPACT_CLASS_MAP[cls]
    title = span.get("title", "")
    if title:
        for keyword in ("High", "Medium", "Low", "Non-economic"):
            if keyword.lower() in title.lower():
                return keyword
    return None


def _parse_rows(html: str) -> List[dict]:
    soup = BeautifulSoup(html, "html.parser")

    # Iterate ALL <tr> elements so we never miss day-breaker rows
    # regardless of their exact class names.
    all_rows = soup.find_all("tr")

    events = []
    current_date: Optional[str] = None

    for row in all_rows:
        # Pick up date from any row that carries a .calendar__date cell
        date_el = row.select_one(".calendar__date")
        if date_el:
            raw = date_el.get_text(strip=True)
            parsed = _parse_date(raw)
            if parsed:
                current_date = parsed

        currency = _text(row.select_one(".calendar__currency"))
        event_name = _text(row.select_one(".calendar__event"))

        if not currency and not event_name:
            continue

        events.append({
            "date":     current_date,
            "time":     _text(row.select_one(".calendar__time")),
            "currency": currency,
            "impact":   _impact(row),
            "event":    event_name,
            "actual":   _text(row.select_one(".calendar__actual")),
            "forecast": _text(row.select_one(".calendar__forecast")),
            "previous": _text(row.select_one(".calendar__previous")),
        })

    return events


def _upsert_events(session: Session, events: List[dict]) -> int:
    """
    Upsert Medium/High impact events.
    Unique key: (currency, event_name, date).
    On conflict: update actual, forecast, previous, time, fetched_at.
    Returns count of rows upserted.
    """
    to_store = [e for e in events if e.get("impact") in STORED_IMPACTS]
    if not to_store:
        return 0

    now = datetime.utcnow()
    rows = [
        {
            "currency":   e["currency"],
            "event_name": e["event"],
            "date":       e["date"],
            "time":       e["time"],
            "impact":     e["impact"],
            "actual":     e["actual"],
            "forecast":   e["forecast"],
            "previous":   e["previous"],
            "fetched_at": now,
        }
        for e in to_store
    ]

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
    session.execute(stmt)
    session.commit()
    return len(rows)


@router.get("/calendar", response_model=List[ForexEvent])
async def get_calendar(
    week: Optional[str] = Query(default="this week", description="this week | next week | last week"),
    session: Session = Depends(get_session),
):
    """
    Scrape ForexFactory calendar for the given week.
    Medium and High impact events are upserted into the database.
    All scraped events (including Low / Non-economic) are returned.
    """
    ff_week = _ff_week_param(week)
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            r = await client.get(
                "https://www.forexfactory.com/calendar",
                params={"week": ff_week},
                headers=FF_HEADERS,
                timeout=20.0,
            )
            r.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=502, detail=f"ForexFactory returned {e.response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=502, detail=f"Failed to reach ForexFactory: {e}")

    events = _parse_rows(r.text)
    if not events:
        raise HTTPException(status_code=502, detail="No calendar rows found — page structure may have changed")

    _upsert_events(session, events)
    return events


@router.get("/events", response_model=List[ForexFactoryEvent])
def get_stored_events(
    currency: Optional[str] = Query(default=None, description="Filter by currency, e.g. USD"),
    impact: Optional[str] = Query(default=None, description="High | Medium"),
    session: Session = Depends(get_session),
):
    """Query Medium/High impact events stored in the database."""
    stmt = select(ForexFactoryEvent)
    if currency:
        stmt = stmt.where(ForexFactoryEvent.currency == currency.upper())
    if impact:
        stmt = stmt.where(ForexFactoryEvent.impact == impact.capitalize())
    return session.exec(stmt).all()
