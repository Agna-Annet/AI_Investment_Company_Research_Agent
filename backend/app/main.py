from fastapi import FastAPI#import FastAPI application class
from fastapi.middleware.cors import CORSMiddleware#utility to control frontend communcation with backend
from app.db.database import Base, engine #Base: registry conatining all models, engine: actual connectionthat speaks to your specific database
from app.api.routes import company, news, analysis, history

Base.metadata.create_all(bind=engine) #Automatically on startup, instructs SQLAlchemy to check if models exist in your db, if not immediately generate them

app = FastAPI(
    title="Company Research Assistant",
    description="API for fetching company info, news, and LLM investment analysis",
    version="1.0.0",
)

# Allow Streamlit (running on port 8501) to call this API
#Browsers enforce strict security blocking websites on one domain (like a Streamlit app running on port 8501) from silently making API calls to another domain (like your FastAPI backend running on port 8000).
#his configuration explicitly tells your backend server: "It's safe to accept web requests coming from http://localhost:8501. Allow them to use any HTTP method (["*"] like GET or POST) and pass along any custom HTTP headers (["*"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(company.router, prefix="/company", tags=["Company"]) #prefix: Prepends this string to every URL inside that router.
app.include_router(news.router, prefix="/news", tags=["News"]) #tags: Groups related endpoints together in the automatic documentation page for readability.
app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
app.include_router(history.router, prefix="/history", tags=["History"])

@app.get("/")
def root():
    return {"message": "Company Research Assistant API is running"}