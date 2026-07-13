import streamlit as st

def render_company_card(data: dict):
    st.subheader(f"{data['name']} ({data['ticker']})")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Sector", data.get("sector") or "N/A")
        st.metric("Industry", data.get("industry") or "N/A")

    with col2:
        market_cap = data.get("market_cap")
        if market_cap:
            st.metric("Market Cap", f"${market_cap:,}")
        else:
            st.metric("Market Cap", "N/A")
        st.metric("P/E Ratio", data.get("pe_ratio") or "N/A")

    with col3:
        st.metric("52W High", data.get("fifty_two_week_high") or "N/A")
        st.metric("52W Low", data.get("fifty_two_week_low") or "N/A")

    if data.get("description"):
        with st.expander("About the company"):
            st.write(data["description"])

    if data.get("website"):
        st.markdown(f"[Visit website]({data['website']})")