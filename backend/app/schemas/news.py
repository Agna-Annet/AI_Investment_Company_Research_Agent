from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NewsArticleResponse(BaseModel):
    id: int
    title: str
    title: str
    source: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[datetime] = None
    summary: Optional[str] = None
    class Config:
        from_attributes = True


class NewsListResponse(BaseModel):
    ticker: str
    articles: list[NewsArticleResponse]
    total: int