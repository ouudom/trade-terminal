from __future__ import annotations

import re
from datetime import datetime, timedelta
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from sqlmodel import Session

from app.core.exceptions import ExternalServiceError, ScrapingError
from app.models.forexfactory_event import ForexFactoryEvent
from app.repositories.forexfactory_repository import ForexFactoryRepository
from app.schemas.forexfactory import ForexEvent


_IMPACT_CLASS_MAP = {
    "icon--ff-impact-red": "High",
    "icon--ff-impact-ora": "Medium",
    "icon--ff-impact-yel": "Low",
    "icon--ff-impact-gra": "Non-economic",
}

FF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "https://www.forexfactory.com/",
    "Accept": "text/html,application/xhtml+xml",
}


def _text(el) -> Optional[str]:
    if el is None:
        return None
    t = el.get_text(strip=True)
    return t if t else None


def _ff_week_param(week: str) -> str:
    today = datetime.utcnow().date()
    days_since_sunday = (today.weekday() + 1) % 7
    this_sunday = today - timedelta(days=days_since_sunday)

    if week == "last week":
        start = this_sunday - timedelta(weeks=1)
    elif week == "next week":
        start = this_sunday + timedelta(weeks=1)
    else:
        start = this_sunday

    return start.strftime("%b%d.%Y").lower()


def _parse_date(raw: Optional[str]) -> Optional[str]:
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


def _parse_rows(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    all_rows = soup.find_all("tr")

    events = []
    current_date: Optional[str] = None

    for row in all_rows:
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


class ForexFactoryService:
    def __init__(self, session: Session) -> None:
        self._repo = ForexFactoryRepository(session)

    async def fetch_calendar(self, week: str = "this week") -> list[ForexEvent]:
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
            raise ExternalServiceError(
                "ForexFactory", f"returned {e.response.status_code}"
            ) from e
        except httpx.RequestError as e:
            raise ExternalServiceError("ForexFactory", f"request failed: {e}") from e

        events = _parse_rows(r.text)
        if not events:
            raise ScrapingError(
                "ForexFactory", "no calendar rows found — page structure may have changed"
            )

        self._repo.upsert_events(events)
        return [ForexEvent(**e) for e in events]

    def get_stored_events(
        self, currency: Optional[str] = None, impact: Optional[str] = None
    ) -> list[ForexFactoryEvent]:
        return self._repo.get_events(currency, impact)
