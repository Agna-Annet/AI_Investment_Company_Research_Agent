import streamlit as st
from utils.api_client import get_company, get_news
from components.company_card import render_company_card
from components.news_feed import render_news_feed
from components.charts import render_price_chart

st.set_page_config(page_title="Search Company", page_icon="🔍")
st.title("🔍 Company Search")

ticker_input = st.text_input(
    "Enter stock ticker symbol",
    placeholder="e.g. AAPL, TSLA, RELIANCE.NS",
    max_chars=20,
).upper().strip()

if st.button("Search", type="primary") and ticker_input:
    with st.spinner("Fetching company data..."):
        try:
            company_data = get_company(ticker_input)
            render_company_card(company_data)
            render_price_chart(ticker_input)
        except Exception as e:
            st.error(f"Could not find company: {e}")

    with st.spinner("Loading news..."):
        try:
            news_data = get_news(ticker_input)
            render_news_feed(news_data)
        except Exception as e:
            st.warning(f"Could not load news: {e}")