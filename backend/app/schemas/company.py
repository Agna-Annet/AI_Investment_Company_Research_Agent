from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CompanyResponse(BaseModel):
    id : int
    ticker : str
    name : str
    sector : Optional[str] = None
    industry : Optional[str] = None
    country : Optional[str] = None
    website : Optional[str] = None
    description : Optional[str] = None
    market_cap : Optional[int] = None
    pe_ratio : Optional[float] = None
    dividend_yield : Optional[float] = None
    fifty_two_week_high : Optional[float] = None
    fifty_two_week_low : Optional[float] = None
    fetched_at : datetime

    class Config:
        from_attributes = True
        