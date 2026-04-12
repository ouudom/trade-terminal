from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import httpx
from app.core.config import settings

router = APIRouter(prefix="/news", tags=["news"])

NEWS_API_BASE = "https://newsapi.org/v2"


@router.get("/top-headlines")
async def top_headlines(
    q: Optional[str] = Query(default=None, description="Keywords to search for"),
    category: Optional[str] = Query(default=None, description="Category: business, entertainment, health, science, sports, technology"),
    country: str = Query(default="us", description="2-letter ISO country code"),
    page_size: int = Query(default=20, le=100, description="Number of results (max 100)"),
):
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "country": country,
        "pageSize": page_size,
    }
    if q:
        params["q"] = q
    if category:
        params["category"] = category

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_BASE}/top-headlines", params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()


@router.get("/everything")
async def everything(
    q: Optional[str] = Query(default=None, description="Keywords or phrases to search for"),
    sources: Optional[str] = Query(default=None, description="Comma-separated news source IDs"),
    domains: Optional[str] = Query(default=None, description="Comma-separated domains to restrict search"),
    from_date: Optional[str] = Query(default=None, alias="from", description="Oldest article date (ISO 8601, e.g. 2024-01-01)"),
    to_date: Optional[str] = Query(default=None, alias="to", description="Newest article date (ISO 8601)"),
    language: str = Query(default="en", description="2-letter ISO language code"),
    sort_by: str = Query(default="publishedAt", alias="sortBy", description="Sort by: relevancy, popularity, publishedAt"),
    page_size: int = Query(default=20, le=100, description="Number of results (max 100)"),
    page: int = Query(default=1, description="Page number"),
):
    params = {
        "apiKey": settings.NEWS_API_KEY,
        "language": language,
        "sortBy": sort_by,
        "pageSize": page_size,
        "page": page,
    }
    if q:
        params["q"] = q
    if sources:
        params["sources"] = sources
    if domains:
        params["domains"] = domains
    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{NEWS_API_BASE}/everything", params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.json())

    return response.json()
