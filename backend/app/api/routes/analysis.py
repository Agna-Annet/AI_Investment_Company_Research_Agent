from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.services.analysis_service import get_or_generate_analysis
from app.schemas.analysis import AnalysisRequest, AnalysisResponse

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
def generate_analysis(request: AnalysisRequest, db: Session = Depends(get_db)):
    try:
        analysis= get_or_generate_analysis(request.ticker, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return analysis