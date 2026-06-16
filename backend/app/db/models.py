from sqlalchemy import Column, Integer, String, Float, BigInteger, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base

class Company(Base):
    __tablename__="companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    sector = Column(String(100))
    industry = Column(String(100))
    country = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    market_cap = Column(BigInteger)
    pe_ratio = Column(Float)
    dividend_yield = Column(Float)
    fifty_two_week_high = Column(Float)
    fifty_two_week_low = Column(Float)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class SearchHistory(Base):
    __tablename__ = "search_history"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20),nullable=False)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())

class NewsArticle(Base):
    __tablename__="news_articles"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    source = Column(String(100))
    url = Column(Text)
    published_at = Column(DateTime)
    summary = Column(Text)
    sentiment = Column(String(20))
    fetched_at = Column(DateTime, server_default=func.now())

class Analysis(Base):
    __tablename__="analyses"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(20), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    summary = Column(Text)
    pros = Column(Text)
    cons = Column(Text)
    verdict = Column(String(50))
    confidence = Column(Float)
    model_used = Column(String(100))
    prompt_tokens= Column(Integer)
    created_at = Column(DateTime, server_default=func.now())