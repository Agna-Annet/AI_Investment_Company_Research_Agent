import requests

BASE_URL = "http://localhost:8000"

def get_company(ticker: str) -> dict:
    response = requests.get(f"{BASE_URL}/company/{ticker}")
    response.raise_for_status()
    return response.json()

def get_news(ticker: str) -> dict:
    response = requests.get(f"{BASE_URL}/news/{ticker}")
    response.raise_for_status()#If the backend returned a successful 200 OK, it does nothing. If it threw a 404 Not Found or a 500 Error, this line immediately raises a Python exception so your frontend knows something failed.
    return response.json() #Automatically parses the raw incoming text-based JSON payload back into a native Python dictionary.

def get_analysis(ticker: str) -> dict:
    response = requests.post(
        f"{BASE_URL}/analysis/",
        json={"ticker": ticker}
    )
    response.raise_for_status()
    return response.json()

def get_history(limit: int = 20) -> list:
    response = requests.get(f"{BASE_URL}/history/", params={"limit": limit})
    response.raise_for_status()
    return response.json()