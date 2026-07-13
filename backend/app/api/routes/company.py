from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.company_service import get_or_fetch_company
from app.services.news_service import fetch_and_store_news
from app.db.models import SearchHistory
from app.schemas.company import CompanyResponse

router = APIRouter()

@router.get("/{ticker}",response_model=CompanyResponse) #decorator that tells FastAPI that this function handles an HTTP GET request.
def get_company(ticker:str, db: Session = Depends(get_db)): #Dependcy injection by Depends, freezes the request to execute get_db before get_company
    try:
        company= get_or_fetch_company(ticker, db)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Company not found: {str(e)}")

    history_entry = SearchHistory(ticker=ticker.upper(), company_id=company.id)
    db.add(history_entry)
    db.commit()

    return company#FastAPI intercepts this return value runs it throigh the CompanyResponse schema validation and translates it to a JSON object to be sent to user's browser.

