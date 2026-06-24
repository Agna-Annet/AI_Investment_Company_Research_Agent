import requests #Libarary to make HTTP requests
from sqlalchemy.orm import Session #Session manages the connection and transactions to your database
from datetime import datetime, timedelta #handles time
from app.db.models import NewsArticle #imports custom database model
from app.config import settings #used to get news api key

CACHE_HOURS = 2

def fetch_and_store_news(ticker: str, company_name: str, db: Session) -> list[NewsArticle]:
    # Check if we have recent news in the database
    cutoff = datetime.utcnow() - timedelta(hours=CACHE_HOURS) #gives time 2 hours before from now
    cached =( 
        db.query(NewsArticle)#select from Newsarticle table
        .filter(NewsArticle.ticker == ticker,NewsArticle.fetched_at >= cutoff) #where ticker=ticker and fetched_at>=cutoff
        .order_by(NewsArticle.published_at.desc())#sort by date of publshing newest first
        .limit(10) #take top 10 results
        .all()
    )

    if cached:
        return cached #if query has results returns it no need of api call

    # If not, fetch from NewsAPI
    url = "https://newsapi.org/v2/everything" #endpoint of NewsAPI service
    params = {  #search criteria
        "q": company_name,
        "sortBy": "publishedAt",
        "pageSize": 10,
        "language": "en",
        "apiKey": settings.NEWS_API_KEY,
    }
    response = requests.get(url, params=params) #sends the actual request to NewsAPI
    response.raise_for_status() #if API call failed this line crashes code with an error
    articles_data = response.json().get("articles", []) #.json() coverts json to dict format now the articles key is fetched and values are stored to a list

    #Save to database
    articles = []
    for item  in articles_data:
        published_at= None
        if item.get("publishedAt"):     #NewsAPI dends dates in ISO format, this block converts string into Python datetime obj so that datebase can understand
            published_at = datetime.fromisoformat(
                item["publishedAt"].replace("Z","+00:00")
            )

        article = NewsArticle(
            ticker=ticker,
            title=item.get("title",""),
            source=item.get("source", {}).get("name"),
            url=item.get("url"),
            published_at=published_at,
            summary=item.get("description"),
            sentiment=None, #LLM decide later
        )
        db.add(article)
        articles.append(article)
    
    db.commit()

    for a in articles:
        db.refresh(a) #updates each object with its new database ID 
    return articles


       


