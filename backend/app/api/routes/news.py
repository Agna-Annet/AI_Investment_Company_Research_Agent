from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.company_service import get_or_fetch_company
from app.services.news_service import fetch_and_store_news
from app.schemas.news import NewsListResponse

router = APIRouter()

@router.get("/{ticker}", response_model=NewsListResponse)
def get_news(ticker: str, db: Session= Depends(get_db)):
    try:
        company= get_or_fetch_company(ticker, db)
        articles= fetch_and_store_news(ticker.upper(), company.name, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return NewsListResponse(
        ticker=ticker.upper(),
        articles=articles,
        total=len(articles)

    )
