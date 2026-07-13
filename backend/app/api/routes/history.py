from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.db.models import SearchHistory, Company

router= APIRouter()

@router.get("/")
def get_search_history(limit: int=20, db: Session = Depends(get_db)):
    results = (
        db.query(SearchHistory)
        .order_by(SearchHistory.searched_at.desc())
        .limit(limit)#for pagination
        .all()
    )

    return [ #manual serialization
        {
            "id": r.id,
            "ticker": r.ticker,
            "searched_at": r.searched_at,
        }
        for r in results
    ]