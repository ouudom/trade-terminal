from __future__ import annotations

from typing import Optional

import httpx

from app.core.config import settings
from app.core.exceptions import ExternalServiceError

NEWS_API_BASE = "https://newsapi.org/v2"


class NewsService:
    async def top_headlines(
        self,
        q: Optional[str] = None,
        category: Optional[str] = None,
        country: str = "us",
        page_size: int = 20,
    ) -> dict:
        params: dict = {
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
            raise ExternalServiceError("NewsAPI", str(response.json()))
        return response.json()

    async def everything(
        self,
        q: Optional[str] = None,
        sources: Optional[str] = None,
        domains: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 20,
        page: int = 1,
    ) -> dict:
        params: dict = {
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
            raise ExternalServiceError("NewsAPI", str(response.json()))
        return response.json()
