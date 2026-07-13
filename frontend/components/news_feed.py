import streamlit as st
from datetime import datetime

SENTIMENT_COLORS = {
    "positive": "🟢",
    "negative": "🔴",
    "neutral": "🟡",
    None: "⚪",
}

def render_news_feed(news_data: dict):
    articles = news_data.get("articles", [])
    if not articles:
        st.info("No recent news found.")
        return

    st.subheader(f"Latest News — {news_data['ticker']}")
    for article in articles:
        sentiment = article.get("sentiment")
        icon = SENTIMENT_COLORS.get(sentiment, "⚪")
        with st.container():
            st.markdown(f"**{icon} {article['title']}**")
            if article.get("source"):
                st.caption(f"Source: {article['source']}")
            if article.get("summary"):
                st.write(article["summary"])
            if article.get("url"):
                st.markdown(f"[Read more]({article['url']})")
            st.divider()