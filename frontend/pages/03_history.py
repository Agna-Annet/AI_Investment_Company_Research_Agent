import streamlit as st
from utils.api_client import get_history

st.set_page_config(page_title="Search History", page_icon="🕒")
st.title("🕒 Search History")

try:
    history = get_history(limit=30)
    if not history:
        st.info("No searches yet. Go search for a company!")
    else:
        for item in history:
            searched_at = item.get("searched_at", "")[:10]
            st.markdown(f"**{item['ticker']}** — {searched_at}")
except Exception as e:
    st.error(f"Could not load history: {e}")