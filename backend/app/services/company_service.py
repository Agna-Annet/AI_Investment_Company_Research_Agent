import yfinance as yf #library to get stock market data 
from sqlalchemy.orm import Session #imports database session
from datetime import datetime, timedelta #handles time values
from app.db.models import Company #imports our database model

CACHE_HOURS = 6

def get_or_fetch_company(ticker: str, db: Session) -> Company:
    ticker = ticker.upper().strip() #cleans up given ticker input

    #Check if we already have fresh data in the database
    existing = db.query(Company).filter(Company.ticker==ticker).first() #.first() returns obj if found else None
    if existing:
        age = datetime.utcnow() - existing.fetched_at
        if age < timedelta(hours=CACHE_HOURS): #if data stored within cache_hours it is returned and func exited
            return existing #return cached version
        
    #Fetch new data from yfinance
    info = yf.Ticker(ticker).info #.info() pulls a massive dictionary of metadata with the ticker value

    data = {
        "ticker": ticker,
        "name": info.get("longName") or info.get("shortName") or ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "country": info.get("country"),
        "website" : info.get("website"),
        "description" : info.get("longBusinessSummary"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "dividend_yield": info.get("dividendYield"),
        "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
        "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
        "fetched_at": datetime.utcnow()
    }

    if existing:
        #update existing record
        for key, value in data.items():
            setattr(existing, key, value) #dynamically updates given attribute (as key) with given value in database
    else:
        #create new record
        existing = Company(**data) #** unpacks dictionary passing key and values to create a new row.
        db.add(existing) #inserts the row

    db.commit() #executes insert and finalizes
    db.refresh(existing) #reloads to populate its primary key ID
    return existing
