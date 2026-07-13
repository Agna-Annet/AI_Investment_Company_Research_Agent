from sqlalchemy.orm import Session #to get a db session to communicate with db
from datetime import datetime, timedelta#to handle time related operations
from app.db.models import Analysis#Analysis class that represents the table model
from app.services.company_service import get_or_fetch_company#to get company details, custom function
from app.services.news_service import fetch_and_store_news#to get company related news, custom function
from app.core.prompts import build_investment_prompt#imports the custom prompt 
from app.core.llm import generate_analysis#imports the function that gets llm service

CACHE_HOURS = 12

def get_or_generate_analysis(ticker: str, db: Session) -> Analysis:
    ticker=ticker.upper().strip()

    cutoff = datetime.utcnow() - timedelta(hours=CACHE_HOURS)#to find the point time beyond which the data becomes stale
    cached = (
        db.query(Analysis)
        .filter(Analysis.ticker == ticker, Analysis.created_at >= cutoff)
        .order_by(Analysis.created_at.desc())
        .first()#returns the first row if existing else None
    )

    if cached:
        return cached
    
    company = get_or_fetch_company(ticker, db)#get comapny data 
    news_articles = fetch_and_store_news(ticker,company.name, db)#get news related to the company
    headlines = [a.title for a in news_articles if a.title]#collect only the news headlines

    company_dict = {
        "name": company.name,
        "sector": company.sector,
        "industry": company.industry,
        "market_cap": company.market_cap,
        "pe_ratio": company.pe_ratio,
        "dividend_yield": company.dividend_yield,
        "fifty_two_week_high": company.fifty_two_week_high,
        "fifty_two_week_low": company.fifty_two_week_low,
        "description": company.description
    }

    prompt=build_investment_prompt(company_dict,headlines)#creating the prompt to get analysis from llm
    result= generate_analysis(prompt)#get the result from the llm

    analysis = Analysis( #store the analysis data in the database
        ticker=ticker,
        company_id=company.id,
        summary=result["summary"],
        pros=result["pros"],
        cons=result["cons"],
        verdict=result["verdict"],
        confidence=result["confidence"],
        model_used=result["model_used"],
        prompt_tokens=result["prompt_tokens"],
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)#forces app to reload the data from database into this variable i.e fields like rowID is available
    return analysis

