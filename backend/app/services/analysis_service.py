from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.models import Analysis
from app.services.company_service import get_or_fetch_company
from app.services.news_service import fetch_and_store_news
from app.core.prompts import build_investment_prompt
from app.core.llm import generate_analysis

CACHE_HOURS = 12

def get_or_generate_analysis(ticker: str, db: Session) -> Analysis;
    ticker=ticker.upper().strip()

    cutoff = datetime.utcnow() - timedelta(hours=CACHE_HOURS)
    cached = (
        db.query(Analysis)
        .filter(Analysis.ticker == ticker, Analysis.created_at >= cutoff)
        .order_by(Analysis.created_at.desc())
        .first()
    )

    if cached:
        return cached
    
    #Gather data
    company = get_or_fetch_company(ticker, db)
    news_articles = fetch_and_store_news(ticker,company.name, db)
    headlines = [a.title for a in news_articles if a.title]

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

    prompt=build_investment_prompt(company_dict,headlines)
    result= generate_analysis(prompt)

    analysis = Analysis(
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
    db.refresh(analysis)
    return analysis

