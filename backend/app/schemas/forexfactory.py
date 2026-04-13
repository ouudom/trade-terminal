"""
Pydantic response schemas for the ForexFactory endpoints.
Extracted from app/routers/forexfactory.py.
"""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ForexEvent(BaseModel):
    date: Optional[str] = None
    time: Optional[str] = None
    currency: Optional[str] = None
    impact: Optional[str] = None
    event: Optional[str] = None
    actual: Optional[str] = None
    forecast: Optional[str] = None
    previous: Optional[str] = None
