import streamlit as st
from utils.api_client import get_analysis

st.set_page_config(page_title="Investment Analysis", page_icon="📊")
st.title("📊 Investment Analysis")
st.caption("Powered by Gemini AI — not financial advice.")

ticker_input = st.text_input(
    "Enter ticker for AI analysis",
    placeholder="e.g. AAPL",
).upper().strip()

if st.button("Generate Analysis", type="primary") and ticker_input:
    with st.spinner("Asking Gemini to analyze..."):
        try:
            result = get_analysis(ticker_input)

            verdict = result.get("verdict", "N/A")
            confidence = result.get("confidence", 0)

            # Verdict color
            color_map = {
                "BUY": "green",
                "HOLD": "orange",
                "AVOID": "red",
                "RESEARCH MORE": "blue",
            }
            color = color_map.get(verdict, "gray")
            st.markdown(
                f"## Verdict: :{color}[{verdict}]  "
                f"(Confidence: {confidence:.0%})"
            )

            st.subheader("Summary")
            st.write(result.get("summary", ""))

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("✅ Pros")
                pros = result.get("pros", "")
                for pro in pros.split("|"):
                    st.markdown(f"- {pro.strip()}")

            with col2:
                st.subheader("⚠️ Cons")
                cons = result.get("cons", "")
                for con in cons.split("|"):
                    st.markdown(f"- {con.strip()}")

            st.caption(
                f"Model: {result.get('model_used')} · "
                f"Generated: {result.get('created_at', '')[:10]}"
            )

        except Exception as e:
            st.error(f"Analysis failed: {e}")