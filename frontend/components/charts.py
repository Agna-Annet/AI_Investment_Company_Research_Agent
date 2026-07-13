import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def render_price_chart(ticker: str):
    st.subheader("Price History (6 months)")
    try:
        data = yf.Ticker(ticker).history(period="6mo")
        if data.empty:
            st.warning("No price data available.")
            return

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data["Close"],
            mode="lines",
            name="Close Price",
            line=dict(color="#4F8EF7", width=2),
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            height=350,
            margin=dict(l=0, r=0, t=20, b=0),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load chart: {e}")