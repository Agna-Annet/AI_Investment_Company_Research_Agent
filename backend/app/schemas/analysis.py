from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnalysisRequest(BaseModel):
    ticker: str

class AnalysisResponse(BaseModel):
    id : int
    ticker: str
    summary: str
    pros: Optional[str] = None
    cons: Optional[str] = None
    verdict: Optional[str] = None
    confidence: Optional[float] = None
    model_used: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True