import streamlit as st

st.set_page_config(
    page_title="Company Research Assistant",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Company Research Assistant")
st.markdown("""
Welcome! Use the sidebar to navigate:

- **Search** — Look up any company by ticker symbol
- **Analysis** — Get an AI-powered investment summary
- **History** — View your recent searches

> ⚠️ This tool is for educational purposes only. Nothing here is financial advice.
""")