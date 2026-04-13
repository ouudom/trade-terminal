from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Query

from app.core.dependencies import get_news_service
from app.services.news_service import NewsService

router = APIRouter(prefix="/news", tags=["news"])


@router.get("/top-headlines")
async def top_headlines(
    q: Optional[str] = Query(default=None, description="Keywords to search for"),
    category: Optional[str] = Query(default=None, description="business, entertainment, health, science, sports, technology"),
    country: str = Query(default="us", description="2-letter ISO country code"),
    page_size: int = Query(default=20, le=100, description="Number of results (max 100)"),
    svc: NewsService = Depends(get_news_service),
):
    return await svc.top_headlines(q=q, category=category, country=country, page_size=page_size)


@router.get("/everything")
async def everything(
    q: Optional[str] = Query(default=None),
    sources: Optional[str] = Query(default=None),
    domains: Optional[str] = Query(default=None),
    from_date: Optional[str] = Query(default=None, alias="from"),
    to_date: Optional[str] = Query(default=None, alias="to"),
    language: str = Query(default="en"),
    sort_by: str = Query(default="publishedAt", alias="sortBy"),
    page_size: int = Query(default=20, le=100),
    page: int = Query(default=1),
    svc: NewsService = Depends(get_news_service),
):
    return await svc.everything(
        q=q,
        sources=sources,
        domains=domains,
        from_date=from_date,
        to_date=to_date,
        language=language,
        sort_by=sort_by,
        page_size=page_size,
        page=page,
    )
